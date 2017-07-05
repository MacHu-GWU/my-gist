#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Word Count Example in the Simple Python MapReduce Framework

INPUT::
    
    [
        (book_title1, content1),
        (book_title2, content2),
        ...
    ]
    
OUTPUT::
    
    [
        (word1, occurence1),
        (word2, occurence2),
        ...
    ]
"""

from pprint import pprint


class MapReduce(object):

    def __init__(self):
        self.intermediate = dict()
        self.result = list()

    def emit_intermediate(self, key, value):
        """A method storing result from each worker into intermediate.
        """
        try:
            self.intermediate[key].append(value)
        except:
            self.intermediate[key] = [value, ]

    def emit(self, value):
        """A method generate the final output.
        """
        self.result.append(value)

    def execute(self):
        """Execute Map Reduce.
        """
        for record in self.distributter():
            self.mapper(record)

        for key, value in self.intermediate.items():
            self.reducer(key, value)

    def display(self):
        """Display result.
        """
        pprint(self.result)

    def distributter(self, *args, **kwargs):
        """a generator method yield record.

        """
        raise NotImplementedError

    def mapper(self, record, **kwargs):
        """

        :param record:
        """
        raise NotImplementedError

    def reducer(self, key, list_of_values, **kwargs):
        """

        :param key:
        :param list_of_values:
        """
        raise NotImplementedError


data = [
    [
        "milton-paradise.txt",
        "[ Paradise Lost by John Milton 1667 ] Book I Of Man ' s first disobedience , and the fruit Of that forbidden tree whose mortal taste Brought death into the World , and all our woe , With loss of Eden , till one greater Man Restore us , and regain the blissful seat , Sing , Heavenly Muse , that , on the secret top Of Oreb , or of Sinai , didst inspire That shepherd who first taught the chosen seed In the beginning how the heavens and earth Rose out of Chaos : or , if Sion hill Delight thee more , and Siloa ' s brook that flowed Fast by the oracle of God , I thence Invoke thy aid to my adventurous song , That with no middle flight intends to soar Above th ' Aonian mount , while it pursues Things unattempted yet in prose or rhyme ."
    ],
    [
        "edgeworth-parents.txt",
        "[ The Parent ' s Assistant , by Maria Edgeworth ] THE ORPHANS . Near the ruins of the castle of Rossmore , in Ireland , is a small cabin , in which there once lived a widow and her four children . As long as she was able to work , she was very industrious , and was accounted the best spinner in the parish ; but she overworked herself at last , and fell ill , so that she could not sit to her wheel as she used to do , and was obliged to give it up to her eldest daughter , Mary ."
    ],
    [
        "austen-emma.txt",
        "[ Emma by Jane Austen 1816 ] VOLUME I CHAPTER I Emma Woodhouse , handsome , clever , and rich , with a comfortable home and happy disposition , seemed to unite some of the best blessings of existence ; and had lived nearly twenty - one years in the world with very little to distress or vex her . She was the youngest of the two daughters of a most affectionate , indulgent father ; and had , in consequence of her sister ' s marriage , been mistress of his house from a very early period . Her mother had died too long ago for her to have more than an indistinct remembrance of her caresses ; and her place had been supplied by an excellent woman as governess , who had fallen little short of a mother in affection ."
    ],
    [
        "chesterton-ball.txt",
        "[ The Ball and The Cross by G . K . Chesterton 1909 ] I . A DISCUSSION SOMEWHAT IN THE AIR The flying ship of Professor Lucifer sang through the skies like a silver arrow ; the bleak white steel of it , gleaming in the bleak blue emptiness of the evening . That it was far above the earth was no expression for it ; to the two men in it , it seemed to be far above the stars . The professor had himself invented the flying machine , and had also invented nearly everything in it ."
    ],
    [
        "bible-kjv.txt",
        "[ The King James Bible ] The Old Testament of the King James Bible The First Book of Moses : Called Genesis 1 : 1 In the beginning God created the heaven and the earth . 1 : 2 And the earth was without form , and void ; and darkness was upon the face of the deep . And the Spirit of God moved upon the face of the waters . 1 : 3 And God said , Let there be light : and there was light . 1 : 4 And God saw the light , that it was good : and God divided the light from the darkness . 1 : 5 And God called the light Day , and the darkness he called Night . And the evening and the morning were the first day ."
    ],
    [
        "chesterton-thursday.txt",
        "[ The Man Who Was Thursday by G . K . Chesterton 1908 ] To Edmund Clerihew Bentley A cloud was on the mind of men , and wailing went the weather , Yea , a sick cloud upon the soul when we were boys together . Science announced nonentity and art admired decay ; The world was old and ended : but you and I were gay ; Round us in antic order their crippled vices came -- Lust that had lost its laughter , fear that had lost its shame . Like the white lock of Whistler , that lit our aimless gloom , Men showed their own white feather as proudly as a plume . Life was a fly that faded , and death a drone that stung ; The world was very old indeed when you and I were young ."
    ],
    [
        "blake-poems.txt",
        "[ Poems by William Blake 1789 ] SONGS OF INNOCENCE AND OF EXPERIENCE and THE BOOK of THEL SONGS OF INNOCENCE INTRODUCTION Piping down the valleys wild , Piping songs of pleasant glee , On a cloud I saw a child , And he laughing said to me : \" Pipe a song about a Lamb !\" So I piped with merry cheer . \" Piper , pipe that song again ;\" So I piped : he wept to hear . \" Drop thy pipe , thy happy pipe ; Sing thy songs of happy cheer :!\" So I sang the same again , While he wept with joy to hear . \" Piper , sit thee down and write In a book , that all may read .\" So he vanish ' d from my sight ; And I pluck ' d a hollow reed , And I made a rural pen , And I stain ' d the water clear , And I wrote my happy songs Every child may joy to hear ."
    ],
    [
        "shakespeare-caesar.txt",
        "[ The Tragedie of Julius Caesar by William Shakespeare 1599 ] Actus Primus . Scoena Prima . Enter Flauius , Murellus , and certaine Commoners ouer the Stage . Flauius . Hence : home you idle Creatures , get you home : Is this a Holiday ? What , know you not ( Being Mechanicall ) you ought not walke Vpon a labouring day , without the signe Of your Profession ? Speake , what Trade art thou ? Car . Why Sir , a Carpenter Mur . Where is thy Leather Apron , and thy Rule ? What dost thou with thy best Apparrell on ? You sir , what Trade are you ? Cobl . Truely Sir , in respect of a fine Workman , I am but as you would say , a Cobler Mur . But what Trade art thou ? Answer me directly Cob . A Trade Sir , that I hope I may vse , with a safe Conscience , which is indeed Sir , a Mender of bad soules Fla ."
    ],
    [
        "whitman-leaves.txt",
        "[ Leaves of Grass by Walt Whitman 1855 ] Come , said my soul , Such verses for my Body let us write , ( for we are one ,) That should I after return , Or , long , long hence , in other spheres , There to some group of mates the chants resuming , ( Tallying Earth ' s soil , trees , winds , tumultuous waves ,) Ever with pleas ' d smile I may keep on , Ever and ever yet the verses owning -- as , first , I here and now Signing for Soul and Body , set to them my name , Walt Whitman [ BOOK I . INSCRIPTIONS ] } One ' s - Self I Sing One ' s - self I sing , a simple separate person , Yet utter the word Democratic , the word En - Masse ."
    ],
    [
        "melville-moby_dick.txt",
        "[ Moby Dick by Herman Melville 1851 ] ETYMOLOGY . ( Supplied by a Late Consumptive Usher to a Grammar School ) The pale Usher -- threadbare in coat , heart , body , and brain ; I see him now . He was ever dusting his old lexicons and grammars , with a queer handkerchief , mockingly embellished with all the gay flags of all the known nations of the world . He loved to dust his old grammars ; it somehow mildly reminded him of his mortality ."
    ]
]


class WordCount(MapReduce):

    def distributter(self):
        return iter(data)

    def mapper(self, record):
        words = record[1].split()
        for w in words:
            self.emit_intermediate(w, 1)  # emit 1

    def reducer(self, key, list_of_values):
        # key: word
        # value: list of occurrence counts
        total = 0
        for value in list_of_values:
            total += value  # counter + 1
        self.emit((key, total))


if __name__ == "__main__":
    wc = WordCount()
    wc.execute()
    wc.display()