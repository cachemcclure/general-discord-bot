# Import Modules
from random import randint

# Roll Dice
def roll_dice(n_die,die_sz,keep_high_b=0,keep_low_b=0,keep_high=0,keep_low=0,sub=0):
    rollstmp = []
    rolls = []
    rolls_all = []
    sign = (-1)**sub
    for yy in range(int(n_die)):
        rollstmp = rollstmp + [int(randint(1,die_sz))*sign]
    if (keep_high_b == 1) and (keep_high < len(rollstmp)):
        rolls = rolls + sorted(rollstmp,reverse=True)[:keep_high]
        rolls_all = rolls_all + rollstmp
    elif (keep_high_b == 1) and (keep_high >= len(rollstmp)):
        rolls = rolls + sorted(rollstmp,reverse=True)
        rolls_all = rolls_all + rollstmp
    elif (keep_low_b == 1) and (keep_low < len(rollstmp)):
        rolls = rolls + sorted(rollstmp)[:keep_low]
        rolls_all = rolls_all + rollstmp
    elif (keep_low_b == 1) and (keep_low >= len(rollstmp)):
        rolls = rolls + sorted(rollstmp)
        rolls_all = rolls_all + rollstmp
    else:
        rolls = rolls + rollstmp
        rolls_all = rolls_all + rollstmp
#    print(rolls)
#    print(rolls_all)
    return rolls, rolls_all

def roller(msg):
    nn = msg.split('+')
    rolls_all = []
    rolls = []
    mod = 0
    for xx in nn:
        if '-' in xx:
            mm = xx.split('-')
            yy = mm[0]
            yy1 = mm[1]
            keep_high_b = 0
            keep_low_b = 0
            keep_high = 0
            keep_low = 0
            interm = yy.split('d')
            if len(interm) == 2:
                try:
                    n_die = int(interm[0])
                except:
                    n_die = 1
                if 'kh' in interm[1]:
                    temp = interm[1].split('kh')
                    keep_high = int(temp[1])
                    interm[1] = int(temp[0])
                    keep_high_b = 1
                elif 'kl' in interm[1]:
                    temp = interm[1].split('kl')
                    keep_low = int(temp[1])
                    interm[1] = int(temp[0])
                    keep_low_b = 1
                die_sz = int(interm[1])
                rolls_t, rolls_all_t = roll_dice(n_die=n_die,die_sz=die_sz,keep_high_b=keep_high_b,
                          keep_low_b=keep_low_b,keep_high=keep_high,keep_low=keep_low,sub=0)
                rolls = rolls + rolls_t
                rolls_all = rolls_all + rolls_all_t
            elif len(interm) == 1:
                mod = int(interm[0])
            keep_high_b = 0
            keep_low_b = 0
            keep_high = 0
            keep_low = 0
            interm = yy1.split('d')
            if len(interm) == 2:
                try:
                    n_die = int(interm[0])
                except:
                    n_die = 1
                if 'kh' in interm[1]:
                    temp = interm[1].split('kh')
                    keep_high = int(temp[1])
                    interm[1] = int(temp[0])
                    keep_high_b = 1
                elif 'kl' in interm[1]:
                    temp = interm[1].split('kl')
                    keep_low = int(temp[1])
                    interm[1] = int(temp[0])
                    keep_low_b = 1
                die_sz = int(interm[1])
                rolls_t, rolls_all_t = roll_dice(n_die=n_die,die_sz=die_sz,keep_high_b=keep_high_b,
                          keep_low_b=keep_low_b,keep_high=keep_high,keep_low=keep_low,sub=1)
                rolls = rolls + rolls_t
                rolls_all = rolls_all + rolls_all_t
            elif len(interm) == 1:
                mod = int(interm[0]) * -1
        else:
            keep_high_b = 0
            keep_low_b = 0
            keep_high = 0
            keep_low = 0
            interm = xx.split('d')
            if len(interm) == 2:
                try:
                    n_die = int(interm[0])
                except:
                    n_die = 1
                if 'kh' in interm[1]:
                    temp = interm[1].split('kh')
                    keep_high = int(temp[1])
                    interm[1] = int(temp[0])
                    keep_high_b = 1
                elif 'kl' in interm[1]:
                    temp = interm[1].split('kl')
                    keep_low = int(temp[1])
                    interm[1] = int(temp[0])
                    keep_low_b = 1
                die_sz = int(interm[1])
                rolls_t, rolls_all_t = roll_dice(n_die=n_die,die_sz=die_sz,keep_high_b=keep_high_b,
                          keep_low_b=keep_low_b,keep_high=keep_high,keep_low=keep_low,sub=0)
                rolls = rolls + rolls_t
                rolls_all = rolls_all + rolls_all_t
            elif len(interm) == 1:
                mod = interm[0]
#    print(rolls)
#    print(rolls_all)
    return rolls, rolls_all, mod
