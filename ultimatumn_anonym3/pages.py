from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import numpy as np


# Used to generate time outs
# fake wait page
class SendBackWaitPage(Page):
    # Use a poisson distribution to generate timeouts (in seconds)
    # output format is a list, so we select its 1st element (the [0] part)
    timeout_seconds = np.random.poisson(4, 1)[0]

    # You might want to use a different distribution
    # or different parameters to make your game more believable


# Explain and introduce the game
class Intro(Page):
    def is_displayed(self):
        # only shown on first round
        return self.round_number == 1

# Page where player chooses its offer
class Choice(Page):
    form_model = 'player'
    form_fields = ['Offer']


    def vars_for_template(self):
        return {
            'player_in_previous_rounds': self.player.in_previous_rounds(),
        }
     #before next page, decide which strategy the bot uses and play for the bot

    def before_next_page(self):
        if self.round_number <= Constants.num_rounds /2:
            self.player.Strategy1()
            # during the  second half play RB
        else:
            self.player.Strategy2()

        self.player.set_payoffs()


# IMPORTANT, a player have to wait for someone to play before seeing the results
# Note that all games are independent, it is just to deceive the player in thinking it plays with another human
#class ResultsWaitPage(WaitPage):
#   def after_all_players_arrive(self):
 #       for p in self.group.get_players():
  #          p.set_payoffs()


# Show the results
class ResultsSummary(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        player_in_all_rounds = self.player.in_all_rounds()

        sum_payoff = sum([p.payoff for p in player_in_all_rounds])

        if self.round_number == Constants.num_rounds:
            self.participant.vars['payoff_MP'] = sum_payoff

        return {
            'n_win': int(sum_payoff/100),
            'sum_payoff': sum_payoff,
            'player_in_all_rounds': player_in_all_rounds,
        }

page_sequence = [
    Intro,
    SendBackWaitPage,
    Choice,
    SendBackWaitPage,
    #ResultsWaitPage,
    ResultsSummary,
]