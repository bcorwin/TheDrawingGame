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
    
    def view_game(self):
        link = settings.BASE_URL + "/view/" + self.game_code
        link = "<a href='" + link + "'>" + self.game_code + "</a>"
        return(link)
    view_game.allow_tags = True
    
    def get_prev_round(self):
        rounds = Round.objects.filter(game=self).order_by('-round_number').exclude(update_status=-1)
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
        return([r.email_address for r in Round.objects.filter(game=self)])
        
    def send_round_over_email(self):
        subject = "Your Drawing Game is over!"
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
        self.save()
        
    def view_round(self):
        link = settings.BASE_URL + "/game/" + self.round_code
        link = "<a href='" + link + "'>" + self.round_code+ "</a>"
        return(link)
    view_round.allow_tags = True
    
    def view_submission(self):
        if self.round_type == "P":
            out = '<img  src="data:image/png;base64,' + self.submission + '" width="200">'
            #out = "<a href='" + "www.google.com" + "'>View</a>"
            #out = u"<a href='%s'>View</a>" % 'http://www.google.com'
        else:
            if len(self.submission) > 160:
                out = self.submission[0:159]
                out += "..."
            else:
                out = self.submission
        return(out)
    view_submission.allow_tags = True
        
    def check_email(self):
        emails = Round.objects.filter(game=self.game)
        emails = [r.email_address.upper() for r in emails]
        if self.round_number != self.game.game_length: emails += [self.game.email_address.upper()]

        if self.email_address.upper() in emails:
            raise ValidationError(('').join(["The email address, ", self.email_address, ", has already been used this game."]))
    
    def new_code(self):
        out = self.round_code
        chk = out in [r.round_code for r in Round.objects.all()]
        while(chk == True):
            out = gen_code()
            chk = out in [r.round_code for r in Round.objects.all()]
        return(out)
        
    def reset_round(self, new_email):
        if self.completed == True:
            raise ValidationError("Original user has already completed the round.")
        elif self.update_status == 2:
            new_r = self
            
            self.set_status(-1)
            self.save()
            
            new_r.pk = None
            new_r.email_address = new_email
            new_r.set_status(0)
            new_r.save()
        
    def wait_longer(self):
        if self.update_status == 2: self.send_reminder_email()
        
    def send_request(self):
        self.set_status(2)
    
        subject = self.display_name + " has not completed their round."
        text_content = ""
        html_content = "To give " + self.display_name + " 24 more hours to complete the round, click <a href='" + settings.BASE_URL + "/wait/" + self.round_code + "'>here</a>.<br>"
        html_content += "To send this round to someone new, click <a href='" + settings.BASE_URL + "/reset/" + self.round_code + "'>here</a>."
        
        send_email([self.game.email_address], subject=subject, text_content=text_content, html_content=html_content)
    
    def send_reminder_email(self):
        self.set_status(1)
        
        subject = "Don't forget to play The Drawing Game round that " + self.display_name + " sent you!"
        text_content = ""
        html_content = "To play your round, click <a href='" + settings.BASE_URL + "/game/" + self.round_code + "'>here</a>."
        
        prev_round = self.game.get_prev_round()
        
        send_email([prev_round.email_address], subject=subject, text_content=text_content, html_content=html_content)
    
    def send_new_round_email(self):
        subject = self.display_name + " has send you a Drawing Game round!"
        text_content = ""
        html_content = "To play your round, click <a href='" + settings.BASE_URL + "/game/" + self.round_code + "'>here</a>."
        
        send_email([self.email_address], subject=subject, text_content=text_content, html_content=html_content)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            g = self.game
            prev_round = g.get_prev_round()
            if prev_round != None:
                self.round_number = prev_round.round_number + 1
                if self.round_number > prev_round.game.game_length: raise ValidationError("Game has been completed. Cannot add another round.")
            else: self.round_number = 1
            self.round_code = self.new_code()
            self.check_email()
            
            super(Round, self).save(*args, **kwargs)
            
            #The below should only run if the above save is completed successfully
            
            ##If game is complete, mark it as so
            if self.round_number >= g.game_length:
                g.completed = True
                g.save()
                self.completed = True
                self.save()
                g.send_round_over_email()
            else: self.send_new_round_email()
                
            ##Set previous round to completed
            if prev_round != None:
                prev_round.completed = True
                prev_round.save()
        else:
            super(Round, self).save(*args, **kwargs)
    
    def __str__(self):
        return(self.round_code)