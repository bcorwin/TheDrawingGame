from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone
from game.email import send_email
from random import choice
from string import ascii_letters

def gen_code(n=6):
        return(''.join([choice(ascii_letters) for l in range(n)]))
        
class Game(models.Model):
    game_length = models.PositiveSmallIntegerField(validators=[MinValueValidator(3), MaxValueValidator(15)], default=6)
    email_address = models.EmailField()
    
    game_code = models.CharField(max_length=6, default=gen_code, unique=True)
    completed = models.BooleanField(default=False)
    
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def current_round(self):
        rounds = self.get_rounds(all=False)
        return(len(rounds))
    
    def get_rounds(self, all = False, order = "desc"):
        rounds = Round.objects.filter(game=self)
        rounds = rounds.order_by('-round_number') if order == "desc" else rounds.order_by('round_number')
        if all == False: rounds = rounds.exclude(update_status=-1)
        
        return(rounds)
    
    def view_game(self):
        link = settings.BASE_URL + "/view/" + self.game_code
        link = "<a href='" + link + "'>" + self.game_code + "</a>"
        return(link)
    view_game.allow_tags = True
    
    def get_last_email(self):
        rounds = self.get_rounds()
        if rounds.exists():
            if len(rounds) == 1: return(self.email_address)
            else: return(rounds[1].email_address)
        else: return(None)
    
    def get_prev_round(self):
        rounds = self.get_rounds()
        if rounds.exists(): return(rounds[0])
        else: return(None)
    
    def new_code(self):
        out = self.game_code
        chk = out in [g.game_code for g in Game.objects.all()]
        while(chk == True):
            out = gen_code()
            chk = out in [g.game_code for g in Game.objects.all()]
        return(out)
        
    def get_all_emails(self):
        emails = [R.email_address for R in self.get_rounds(all = True)]
        if self.email_address not in emails: emails = emails + [self.email_address]
        return(emails)
        
    def get_prev_emails(self):
        emails = [R.email_address for R in self.get_rounds(all = False)]
        if self.email_address not in emails: emails = emails + [self.email_address]
        emails.pop(0)
        emails.pop(0)
        return(emails)
        
    def send_round_over_email(self, expired=False):
        subject = "Your Drawing Game is over!" if expired == False else "Your Drawing Game has expired."
        text_content = ""
        html_content = "To view the completed game, click <a href='" + settings.BASE_URL + "/view/" + self.game_code + "'>here</a>."
        
        send_email(self.get_all_emails(), subject=subject, text_content=text_content, html_content=html_content)
        
    def save(self, *args, **kwargs):
        if not self.pk:
            self.game_code = self.new_code()
        super(Game, self).save(*args, **kwargs)
    
    def __str__(self):
        return(self.game_code)
    
class Round(models.Model):
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    game_number = models.PositiveIntegerField()
    
    round_number = models.PositiveSmallIntegerField()
    round_code = models.CharField(max_length=6, default=gen_code, unique=True)
    round_type = models.CharField(max_length=1, choices=(("T", "Text round"), ("P", "Picture round")))
    
    email_address = models.EmailField()
    submission = models.TextField()
    display_name = models.CharField(max_length=32)
    
    update_status = models.SmallIntegerField(default=0, choices=((-2,"Expired"), (-1,"Reset"),(0,"None"),(1,"Reminder sent"),(2,"Request sent")))
    update_status_date = models.DateTimeField(auto_now_add=True)
    
    completed = models.BooleanField(default=False)
    
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
     
    def set_status(self, status):
        self.update_status = status
        self.update_status_date = timezone.now()
        
    def view_round(self):
        link = settings.BASE_URL + "/game/" + self.round_code
        link = "<a href='" + link + "'>" + self.round_code+ "</a>"
        return(link)
    view_round.allow_tags = True
    
    def view_submission(self):
        out = '<img  src="data:image/png;base64,' + self.submission + '" width="500" border="1">' if self.round_type == "P" else self.submission
        return(out)
    view_submission.allow_tags = True
        
    def check_email(self):
        emails = [e.upper() for e in self.game.get_all_emails()]
        if self.email_address.upper() in emails:
            raise ValidationError((', ').join(["The email address", self.email_address, "has already been used this game. <a href='javascript:history.back()'>Go back</a> to try again."]))
    
    def new_code(self):
        out = self.round_code
        chk = out in [r.round_code for r in Round.objects.all()]
        while(chk == True):
            out = gen_code()
            chk = out in [r.round_code for r in Round.objects.all()]
        return(out)
        
    def reset_round(self, new_email):
        out = "Unknown error. Please send feedback."
        if self.completed == True:
            out = "Original user has already completed the round."
        elif self.update_status == 2:
            new_r = Round(  game=self.game,
                            email_address = new_email,
                            round_number = self.round_number,
                            round_type=self.round_type,
                            display_name=self.display_name,
                            submission=self.submission)
            out = new_r.save(is_reset=True)
            
            if out == None:
                self.set_status(-1)
                self.save()
                out = None
        return(out)
        
    def wait_longer(self):
        if self.update_status == 2: self.send_reminder_email()
        
    def send_request(self):
        self.set_status(2)
        self.save()
    
        subject = self.email_address + " has not completed their round."
        text_content = ""           
        html_content = "To give " + self.email_address + " 24 more hours to complete the round, click <a href='" + settings.BASE_URL + "/wait/" + self.round_code + "'>here</a>.<br>"
        html_content += "To send this round to someone new, click <a href='" + settings.BASE_URL + "/reset/" + self.round_code + "'>here</a>."
        
        send_email([self.game.get_last_email()], subject=subject, text_content=text_content, html_content=html_content)
    
    def send_reminder_email(self):
        self.set_status(1)
        self.save()
        
        subject = "Don't forget to play The Drawing Game round that " + self.display_name + " sent you!"
        text_content = ""
        html_content = "To play your round, click <a href='" + settings.BASE_URL + "/game/" + self.round_code + "'>here</a>."
        
        send_email([self.email_address], subject=subject, text_content=text_content, html_content=html_content)
    
    def send_new_round_email(self, is_reset=False):
        subject = self.display_name + " has sent you a Drawing Game round!"
        text_content = ""
        html_content = "To play your round, click <a href='" + settings.BASE_URL + "/game/" + self.round_code + "'>here</a>."
        
        send_email([self.email_address], subject=subject, text_content=text_content, html_content=html_content)
        
        
        if self.round_number > 1 and is_reset == False:            
            subject = self.display_name + " has played their round!"
            to_emails = self.game.get_prev_emails()
            html_content = "When all rounds have been played, you can view your game <a href='" + settings.BASE_URL + "/view/" + self.game.game_code + "'>here</a>."
            
            send_email(to_emails, subject=subject, text_content=text_content, html_content=html_content)
    
    def save(self, is_reset=False, *args, **kwargs):
        if not self.pk:
            g = self.game
            self.game_number = g.pk
            prev_round = None
            if self.round_number == None:
                prev_round = g.get_prev_round()
                if prev_round != None:
                    self.round_number = prev_round.round_number + 1
                    if self.round_number > prev_round.game.game_length: raise ValidationError("Game has been completed. Cannot add another round.")
                else: self.round_number = 1
            self.round_code = self.new_code()
            
            try: self.check_email()
            except ValidationError as e: return(e)
            
            super(Round, self).save(*args, **kwargs)
            
            #The below should only run if the above save is completed successfully
            
            ##If game is complete, mark it as so
            if self.round_number >= g.game_length:
                g.completed = True
                g.save()
                self.completed = True
                self.save()
                g.send_round_over_email()
            else: self.send_new_round_email(is_reset)
                
            ##Set previous round to completed and email previous players
            if prev_round != None:
                prev_round.completed = True
                prev_round.save()                    
        else:
            super(Round, self).save(*args, **kwargs)
        return(None)

    def __str__(self):
        return(self.round_code)