import os
from tools.matching_manager import matching_manager
import pprint as pp

# Frase original do arquivo srt
str1 = u"Olhe, eu sei que alguma garota vai ser sortuda... ...de se tornar a senhora Barry Finkel."

# parte do audio correta, traduzido
str2 = u"Eu sei que algumas garotas vai para ser uma sorte incrivel para se tornar a Sra. Barry Finkel"
# parte do audio erradas
str3 = u"Falou com Barry? Nao consigo parar de sorrir. Percebi. Parece que voce dormiu com um cabide na boca."
str4 = u"Voce se casou quando tinha, sei la, oito? Bem vindo de volta ao mundo! Pegue uma colher!"

class ConsoleGuiManager():
    def LogProgress(self, msg):
        print msg

gui_manager = ConsoleGuiManager()
mm = matching_manager(gui_manager)

print "Testing sentence distance!!\n"

print mm.sentence_distance(str1, str2)
print mm.sentence_distance(str1, str3)
print mm.sentence_distance(str1, str4)

str1 = u'... completely naked.'
str2 = u'naked'
str3 = u"There's nothing to tell!\nHe's just a guy from work!"

print "Testing sentence distance: "
print mm.sentence_distance(str1, str2)
print mm.sentence_distance(str1, str3)

original_subs = [(3000, 3100, u"Nao ha nada para contar! Ele e so um cara do trabalho!"),
        (4000, 4100, u"Voce esta saindo com esse cara!"),
        (4500, 4600, u"Deve ter alguma coisa errada com ele!"),
        (5000, 5100, u"Tudo bem, Joey, vai com calma."),
        (6000, 6100, u"Entao, ele e corcunda? Corcunda e careca?"),
        (7000, 7100, u"Espera ai, ele come giz?"),
        (8000, 8100, u"E que eu nao quero que ela passe pela mesma coisa que eu passei com o Carl!"),
        (9000, 9100, u"Relaxem."),
        (9200, 9300, u"Nao E nem um encontro."),
        (9500, 9600, u"Sao so duas pessoas indo jantar juntas sem fazer sexo.")]

print "\nTesting matching subs trans\n"

print "\nTEST CASE 1 ##############\n"

#Translating subtitles...
#10 out of 10 successful translations.
subs = [
(500, 4600, u"N the h nothing to tell! He's a guy from work!"),
(4800, 7040, u"You're dating this guy!"),
(7200, 9600, u'There must be something wrong with him!'),
(9600, 11680, u'Okay, Joey, take it easy.'),
(12000, 14720, u'Then, he hump? Hunchback and bald?'),
(16200, 18240, u'Wait, he eat chalk?'),
(18600, 21600, u'I do not want her to go through the same thing I went through with Carl!'),
(21600, 23400, u'All right, guys, relax'),
(23400, 25720, u'Relax. N or a date.'),
(25800, 29320, u'S s two people going out to dinner together without having sex.')]
        
#Transcripting speech segments...
#9 out of 9 successful transcriptions.
trans = [
(0, 2915, u"there's nothing to tell it"),
(2901, 4448, u'just some guy I work with'),
(4526, 8581, u'call mom you are going out with a guy that got to be something wrong with them'),
(8427, 10903, u'I like jelly bean ice'),
(11539, 17311, u'so did you have a hard bump and herpes'),
(17437, 20469, u"just as I don't want her to go through what I went through"),
(20316, 21491, u'Ruth Carl'),
(21430, 29014, u"everybody relax relax this is not even a date it's not it's just two people going out to dinner and not having sex")]

pp.pprint(mm.match_subs_trans(subs, trans, original_subs))

'''
HOW SUBS SHOULD ACUTALLY BE MATCHED

(0, 2915, u"there's nothing to tell it"), (2901, 4448, u'just some guy I work with'),
(500, 4600, u"N the h nothing to tell!\nHe's a guy from work!"),

(4526, 8581, u'call mom you are going out with a guy that got to be something wrong with them'),
(4800, 7040, u"You're dating this guy!"), (7200, 9600, u'There must be something wrong with him!'),

(8427, 10903, u'I like jelly bean ice'),
(9600, 11680, u'Okay, Joey, take it easy.'),

(11539, 17311, u'so did you have a hard bump and herpes'),
(12000, 14720, u'Then, he hump?\nHunchback and bald?'),

(17437, 20469, u"just as I don't want her to go through what I went through"), (20316, 21491, u'Ruth Carl'),
(16200, 18240, u'Wait, he eat chalk?'), (18600, 21600, u'I do not want her to go through the same thing I went through with Carl!'),

(21430, 29014, u"everybody relax relax this is not even a date it's not it's just two people going out to dinner and not having sex"),
(21600, 23400, u'All right, guys, relax'), (23400, 25720, u'Relax.\nN or a date.'), (25800, 29320, u'S s two people going out to dinner together without having sex.'),

(29047, 30040, u'')

temporaty matching:
[[0, 1], [], [2], [], [], [], [5, 6], [], [7], [7]]

temporaty matching 2:
[[0], [], [2], [], [], [], [5, 6], [], [7], [7]]

DP matching 
[[0, 1], [0, 1], [2, 3], [2, 3], [4], [4], [5, 6], [5, 6], [7, 8], [7, 8]]

DP matching 2
[[0, 1], [0, 1], [2, 3], [2, 3], [4], [4], [5], [5], [6, 7], [6, 7]]

DP matching 3 
[[0, 1, 2], [0, 1, 2], [0, 1, 2], [3], [4, 5, 6], [4, 5, 6], [4, 5, 6], [7], [7], [7]]

gold matching:
[[0, 1], [2], [2], [3], [4], [5], [5,6], [7], [7], [7]]
'''


##############################################

print "\nTEST CASE 2 ##############\n"

original_subs = [
(500, 4600, 'N\xc3\xa3o h\xc3\xa1 nada para contar! Ele \xc3\xa9 s\xc3\xb3 um cara do trabalho!')
,(4800, 7040, 'Voc\xc3\xaa est\xc3\xa1 saindo com esse cara!')
,(7200, 9600, 'Deve ter alguma coisa\nerrada com ele!')
,(9600, 11680, 'Tudo bem, Joey,\nvai com calma.')
,(12000, 14720, 'Ent\xc3\xa3o, ele \xc3\xa9 corcunda?\nCorcunda e careca?')
,(16200, 18240, 'Espera a\xc3\xad, ele come giz?')
,(18600, 21600, '\xc3\x89 que eu n\xc3\xa3o quero que ela passe pela\nmesma coisa que eu passei com o Carl!')
,(21600, 23400, 'Tudo bem, gente, relaxem')
,(23400, 25720, 'Relaxem.\nN\xc3\xa3o \xc3\xa9 nem um encontro.')
,(25800, 29320, 'S\xc3\xa3o s\xc3\xb3 duas pessoas indo jantar\njuntas sem fazer sexo.')
,(30600, 33500, 'Parece um encontro para mim.')
,(34800, 37800, 'Ent\xc3\xa3o eu estou de volta ao colegial.\nl\xc3\xa1 no meio da lanchonete ...')
,(37800, 40440, '... totalmente pelado.')
,(40800, 42680, 'Ah, sim. J\xc3\xa1 tive o mesmo sonho.')
,(43200, 46400, 'Ent\xc3\xa3o eu olho para baixo e percebo\nque tem um telefone ...')
,(47400, 48920, '... l\xc3\xa1.')
,(51600, 53400, '-Em vez de ...?\n-Isso mesmo!')
,(53400, 55200, 'Nunca tive esse sonho.')
,(55200, 58040, 'De repente, o telefone come\xc3\xa7a a tocar.')
,(59400, 62400, 'Agora, eu n\xc3\xa3o sei o que fazer,\ntodo mundo come\xc3\xa7a a olhar pra mim.')
,(62400, 64880, 'E eles n\xc3\xa3o olhavam antes?')
,(66000, 68680, 'Finalmente, eu penso:\n"\xc3\x89 melhor eu atender".')
,(69600, 71960, 'E \xc3\xa9 minha mae.')
,(73800, 78040, 'O que \xc3\xa9 muito, muito estranho,\nporque ela nunca me liga!')
]

#Translating subtitles...
subs = [
(500, 4600, u"There's nothing to tell! He's just a guy from work!")
,(4800, 7040, u'Are you going out with this guy!')
,(7200, 9600, u'There must be something wrong with him!')
,(9600, 11680, u'Okay, Joey, take it easy.')
,(12000, 14720, u"So he's a hunchback? Hunchback and bald?")
,(16200, 18240, u'Wait a minute, he eat chalk?')
,(18600, 21600, u"Is that I don't want her to go through the same thing I went through with Carl!")
,(21600, 23400, u'All right, guys, relax')
,(23400, 25720, u"Relax. It's not even a date.")
,(25800, 29320, u"It's just two people going out to dinner together without having sex.")
,(30600, 33500, u'Sounds like a date to me.')
,(34800, 37800, u"So I'm back to high school. there in the middle of the cafeteria.")
,(37800, 40440, u'... completely naked.')
,(40800, 42680, u"Oh, Yes. I've had the same dream.")
,(43200, 46400, u'Then I look down and realize I have a phone ...')
,(47400, 48920, u"I don't know...")
,(51600, 53400, u"-Instead of ...?\n-That's right!")
,(53400, 55200, u'Never had this dream.')
,(55200, 58040, u'All of a sudden, the phone starts ringing.')
,(59400, 62400, u"Now, I don't know what to do, everybody starts looking at me.")
,(62400, 64880, u'And they have not looked before?')
,(66000, 68680, u'Finally, I think: "I\'d better meet".')
,(69600, 71960, u'And is my mother.')
,(73800, 78040, u'What is very, very strange, because she never calls me!')
]

#Transcripting speech segments...
trans = [
(0, 2815, u"there's nothing to tell")
,(4626, 8481, u'come on you are going out with the guys I got to be something wrong with them')
,(8527, 10803, u'a jelly bean ice')
,(11639, 17211, u'does he have a hump a hump and a hairpiece')
,(17537, 20369, u'Savannah want to go to go through what I went')
,(20416, 21391, u'Ritz-Carlton')
,(21530, 28914, u'okay black')
,(29147, 39224, u'translate date to me')
,(39503, 41964, u'naked')
,(42846, 45958, u"then I look down and I realize there's a phone")
,(47444, 48140, u'there')
,(51298, 56314, u'instead of a trifle')
,(57010, 58171, u'starts to ring')
,(59193, 62119, u"no I don't know what to do everybody starts looking at")
,(62119, 63605, u'they were looking at you before')
,(65695, 67877, u"find me I figure I'd better answer it")
,(69456, 71268, u"and it turns out it's my mother")
,(71639, 74983, u'which is very very weird because')
]

pp.pprint(mm.match_subs_trans(subs, trans, original_subs))

'''
DP matching 3
[[0], [1, 2], [1, 2], [1, 2], [3], [3], [4, 5], [4, 5], [4, 5], [6, 7], [6, 7], [6, 7], 
[8, 9, 10], [8, 9, 10], [8, 9, 10], [11], [11], [11], [12, 13, 14], [12, 13, 14], 
[12, 13, 14], [15, 16, 17], [15, 16, 17], [15, 16, 17]]

DP matching 3
[[0], [1, 2], [1, 2], [1, 2], [3], [3], [4], [4], [4], [5, 6, 7], [5, 6, 7], [5, 6, 7], [8], [9, 10], [9, 10], [9, 10], [11], [12, 13], [12, 13], [12
, 13], [14], [15], [16], [17]]

gold matching:
[[0],[1],[1],[2],[3],[],[4,5],[6],[6],[6],[7],[],[8],[],[9],[10],[11],[],[12]]


Alignment with comments:

(500, 4600, u"There's nothing to tell! He's just a guy from work!")
(0, 2815, u"there's nothing to tell")

,(4800, 7040, u'Are you going out with this guy!') ,(7200, 9600, u'There must be something wrong with him!')
,(4626, 8481, u'come on you are going out with the guys I got to be something wrong with them')

,(9600, 11680, u'Okay, Joey, take it easy.')
,(8527, 10803, u'a jelly bean ice')

,(12000, 14720, u"So he's a hunchback? Hunchback and bald?")
,(11639, 17211, u'does he have a hump a hump and a hairpiece')


,(16200, 18240, u'Wait a minute, he eat chalk?')
------ What to do here? (Transcription failed)

,(18600, 21600, u"Is that I don't want her to go through the same thing I went through with Carl!")
,(17537, 20369, u'Savannah want to go to go through what I went') ,(20416, 21391, u'Ritz-Carlton')

,(21600, 23400, u'All right, guys, relax') ,(23400, 25720, u"Relax. It's not even a date.") ,(25800, 29320, u"It's just two people going out to dinner together without having sex.")
,(21530, 28914, u'okay black')
------ Trancription failed, but notice the time difference...

,(30600, 33500, u'Sounds like a date to me.')
,(29147, 39224, u'translate date to me')

,(34800, 37800, u"So I'm back to high school. there in the middle of the cafeteria.")
------ What to do here? (Transcription failed)

,(37800, 40440, u'... completely naked.')
,(39503, 41964, u'naked')

,(40800, 42680, u"Oh, Yes. I've had the same dream.")

,(43200, 46400, u'Then I look down and realize I have a phone ...')
,(42846, 45958, u"then I look down and I realize there's a phone")

,(47400, 48920, u"I don't know...")
,(47444, 48140, u'there')
------ Translation completely failed! ???? (maybe using google translate will help)

,(51600, 53400, u"-Instead of ...?\n-That's right!")
,(51298, 56314, u'instead of a trifle')

,(53400, 55200, u'Never had this dream.')
------ What to do here? (Transcription failed)

,(55200, 58040, u'All of a sudden, the phone starts ringing.')
,(57010, 58171, u'starts to ring')

,(59400, 62400, u"Now, I don't know what to do, everybody starts looking at me.")
,(59193, 62119, u"no I don't know what to do everybody starts looking at")

,(62400, 64880, u'And they have not looked before?')
,(62119, 63605, u'they were looking at you before')

,(66000, 68680, u'Finally, I think: "I\'d better meet".')
,(65695, 67877, u"find me I figure I'd better answer it")

,(69600, 71960, u'And is my mother.')
,(69456, 71268, u"and it turns out it's my mother")

,(73800, 78040, u'What is very, very strange, because she never calls me!')
,(71639, 74983, u'which is very very weird because')
------ Final part transcription failed

'''

##############################################

print "\nTEST CASE 3 ##############\n"