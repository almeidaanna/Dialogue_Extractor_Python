import re
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

class Friends:

    def __init__(self):
        """
        Initialise instance variables.
        """
        self.cleanlist = list()

    def extract_dialogue(self):
        """
        Creates a file without the metadata.
        Returns:
        1. a new file with a list of tuples containing the characters and their dialogues.
        """
        newtup = tuple()
        bracket1 = r'\(.*?\)'
        bracket2 = r'\[.*?\]'
        first_Scene = r'.*?\[Scene:.*?\]'
        space = ''
        # utf-8 encodes apostrophy to normal quote
        with open('input_script.txt', encoding='utf-8') as script:
            script_line = script.read()
            # removes the lines before the first scene and the scene sentence as well
            new_script = re.sub(first_Scene, space, script_line, 1, flags=re.DOTALL)
            # removes words/sentences in brackets
        if ('(' in new_script):
            new_script = re.sub(bracket1, space, new_script)
        if ('[' in new_script):
            new_script = re.sub(bracket2, space, new_script)
        new_script = re.sub(' +', ' ', new_script)
        # creates a list of sentences
        script_list = new_script.splitlines()
        # removes the extra spaces in the list
        for item in range(len(script_list)):
            if '' in script_list:
                script_list.remove('')
        # creates a tuple with character and their respective line
        for item in script_list:
            if ':' not in item:
                continue
            else:
                newtup = tuple(item.split(':'))
                self.cleanlist.append(newtup)

        script.close()
        return self.cleanlist

    def separate_dialogue(self):
        """
        Creates files for each characters with their respective dialogues.
        Returns:
        1. multiple character files along with their respective dialogues is generated.
        """
        character = set()
        for item in range(len(self.cleanlist)):
            actor = self.cleanlist[item][0].lower()
            character.add(actor)

        # creates a set of characters to put their respective lines in files with their names
        for actor in character:
            characterfiles = open(f'32313500_{actor}.txt', 'w', encoding='utf-8')
            for i in range(len(self.cleanlist)):
                if actor == self.cleanlist[i][0].lower():
                    newstr = str(self.cleanlist[i][1])
                    characterfiles.write(newstr + '\n')
            characterfiles.close()

class WordFreq:

    def frequency(self):
        """
        Creates a 32313500_data.csv file with the top 5 frequently use words by characters having more than 100 unique words
        Returns:
        1. data frame with the top 5 frquently used words.
        """
        friends_script = Friends()
        cleanlist = friends_script.extract_dialogue()
        character = set()
        wordfreq = list()

        for item in range(len(cleanlist)):
            actor = cleanlist[item][0].lower()
            character.add(actor)

        for actor in character:
            characterfiles = open(f'32313500_{actor}.txt', "r", encoding='utf-8')
            string = characterfiles.read()
            flag = True
            newlist = list()
            uqwords = set()
            # newstr = re.sub(r'[^\w\s]', '', string)#to remove all special characters
            # creates a list of words in small letter
            newstr = string.lower().split()
            # creates a set of unique words
            for word in range(len(newstr)):
                uqwords.add(newstr[word])
            # checking the count of unique words in the list if words
            if len(uqwords) > 100:
                flag = True
            else:
                flag = False

            if flag == True:
                for item in uqwords:
                    count = newstr.count(item)
                    newlist.append([item, count])
            # sorting the list based on the count and reversing it
            for i in range(len(newlist)):
                newlist = sorted(newlist, key=lambda x: x[1])
            newlist = newlist[-5:]

            if newlist == []:
                continue
            else:
                for j in range(len(newlist)):
                    newlist[j].insert(0, actor.lower())

                word_freq_list = newlist[::-1]
                wordfreq.extend(word_freq_list)
            characterfiles.close()
        # placing the rows and columns in a csv file
        df = pd.DataFrame(wordfreq, columns=['role', 'word', 'freq'])
        df.to_csv('32313500_data.csv', index=False)
        return df

    def concat_roleword(self, x_axis):
        return f"({x_axis['role']},{x_axis['word']})"

    def frequency_graph(self):
        """
        Creates multiple graphs of the top 5 frequently use words along with a final graph with all the characters.
        Returns:
        1. graphs for the top 5 frequently used words.
        """
        freq_table = self.frequency()
        freq_table['(role,word)'] = freq_table.apply(self.concat_roleword, axis=1)
        # start and end are the limits used to get top 5 words for each characters
        end = 4
        start = 0
        # color variable is used to traverse throught the list of colours
        color = 0
        colour_list = ['g', 'darksalmon', 'navy', 'pink', 'darkcyan', 'lavender']
        plt.figure(figsize=(15, 15))
        plt.subplots_adjust(hspace=0.6, wspace=0.4)
        # creates a horizontal bar-graph of frequency vs the words.
        while end < len(freq_table):
            role_col = freq_table.loc[start:end, 'role'].values
            word_col = freq_table.loc[start:end, 'word'].values
            freq_col = freq_table.loc[start:end, 'freq'].values
            start = end + 1
            end = end + 5
            plt.subplot(3, 2, color + 1)
            plt.barh(word_col, freq_col, color=colour_list[color])
            plt.xticks(fontsize=10)
            plt.yticks(fontsize=10)
            plt.xlabel('frequency', fontsize=10)
            plt.ylabel('word', fontsize=10)
            plt.xlim(left=0, right=28)
            plt.title('Frequency of the Top 5 Words used by ' + role_col[0], fontsize=15)
            plt.grid(linestyle='--')
            color = color + 1
        plt.show()
        # creates a graph with all the friends characters and their word frequency
        freq_table.plot(kind='bar', color='k', x='(role,word)', y='freq', ylabel='freq',
                        title='Frequency for word used by Friends characters')
        plt.grid(color='aliceblue', linestyle='--')

def main():
    # Task 1
    cleanscript = open('32313500_clean_dialogue.txt', 'w', encoding='utf-8')
    friends_script = Friends()
    print(friends_script.extract_dialogue(), file=cleanscript)
    cleanscript.close()
    # Task 2
    friends_script.separate_dialogue()
    # Task 3
    FriendsWordFreq = WordFreq()
    FriendsWordFreq.frequency()
    # Task 4
    FriendsWordFreq.frequency_graph()


if __name__ == "__main__":
    main()

# A bar graph is generally chosen because of the ease with which it can be read and understood. Its readablity is why I have chosen to use a horizontal bar graph, to represent the words (y-axis) vs the frequency(x-axis) of the words spoken by each character, because it is simple to obtain the readings and also provides the user with all the necessary information just by looking at the graph.
#
# In the graphs plotted for each character, shows the top 5 word along with their frequency of usage. The highest used words by each character are:
#
# i) 'you' by Ross and Monica
#
# ii) 'i' by Phoebe, Joey and Chandler
#
# iii) 'a' by Rachel
#
# From the final graph plotted it is observed that the highest spoken word is 'i' by chandler for about 26 times.
#
