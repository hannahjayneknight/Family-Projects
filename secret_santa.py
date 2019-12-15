'''
Program that allows you to type in the names of the people taking part in 
secret santa. It then allocates them a person to buy for.
'''
import random 
import copy

def main():

    def make_list_people():
        '''
        Makes a list of all the people taking part in secret santa.
        '''
        # makes empty list ready to be filled
        list_people = []

        while True:
            # user inputs a name
            name = input('Enter a name: (blank to quit) ')
            # if no more people to add, code terminates
            if name == '':
                break
            # will add name to the list of people taking part
            else:
                list_people.append(name)
        # returns the final list of participants
        return list_people

    def allocate_secret_santa():
        '''
        Makes a dictionary where the key is the person buying the gift
        and the value is the person they are buying for. 
        '''
        # creates an empty dictionary ready to be filled
        d = {}

        # imports the list of participants by running the other function
        list_people = list(make_list_people())

        # this makes another list for us to remove people from to ensure there are no duplicates
        list_people2 = copy.copy(list_people)

        # runs through each participant in the main list...
        for i in range(len(list_people)):

            # generates a randomly generated person from list 2
            random_person = list_people2[random.randint( 0, len(list_people2)) - 1]

            # checks that a randomly selected person is not the same as the person themself
            if random_person != list_people[i] :

                # if they're not, then the person is added to the dictionary as a key, and their value is the random person
                d.update( {list_people[i]: random_person })

                # removes the person from list2 so they cannot be picked again
                list_people2.remove(random_person)
            else:
                continue
        return d

    print(allocate_secret_santa())

    

if __name__ == "__main__":
    main()

