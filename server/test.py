import random
import configparser


def raffle_award():
    temp_number = random.randint(1, 10)
    print(temp_number)
    if temp_number < 9:
        return 0
    conf = configparser.ConfigParser()
    conf.read('config.ini')
    award_string = conf.get('raffle', 'daily_award')
    if award_string == '0000000000000':
        return 0
    award_array = list(award_string)
    temp = list()
    for index in range(len(award_string)):
        if award_string[index] == '1':
            temp.append(index)
    if temp:
        award_choice = random.choice(temp)
        del temp[temp.index(award_choice)]
        award_array[award_choice] = '0'
        award_string = ''.join(award_array)

    else:
        award_string = '0000000000000'
        award_choice = -1
    conf.set('raffle', 'daily_award', award_string)
    with open('config.ini', 'w') as fp:
        conf.write(fp)
    award_id = award_choice + 1
    return award_id


if __name__ == '__main__':
    a = []
    for i in range(20):
        a.append(raffle_award())
    print(a)
