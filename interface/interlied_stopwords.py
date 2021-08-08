#STOPWORDS
from nltk.corpus import stopwords

def interlied_sw(lang):
    lang_s=""
    lang_s=str(lang)
	
    if (lang_s == "slovene"):
        sw=['a','à','á','ah','ali','bi', 'bil', 'bila', 'bile', 'bili', 'bilo', 'biti', 'blizu', 'bo', 'bodo', 'bojo', 'bolj',
                          'bom', 'bomo', 'boste', 'bova', 'boš', 'brez', 'cel', 'cela', 'celi', 'celo', 'da','de' ,'do', 'dokler',
                          'dva','dve','dolcissimo','eden', 'en','et', 'eni', 'ena', 'ene', 'eno', 'etc', 'espressivo','g.', 'g','ga.', 'ga', 'i', 'idr', 'idr.','itd.', 
                          'itd', 'ii', 'iii','imam','ima','imava','imata','imamo','imajo','imaš','imeti', 'in', 'iv', 'ix', 'iz', 'jaz', 'je', 'ji', 'jih', 'jim', 'jo','ju', 'k','kadar', 'kadarkoli', 'kaj',
                          'kajti', 'kako', 'kakor', 'kamor', 'kamorkoli', 'kar', 'karkoli', 'katerikoli', 'kdaj', 'kdo', 'kdorkoli',
                          'ker', 'ki', 'kje', 'kjer', 'kjerkoli', 'knjim','ko', 'koder', 'koliko','kolikšen','kolikšno','kolikšna','koderkoli', 'koga', 'komu', 'kot', 'kratek', 
                          'kratka', 'kratke', 'kratki','la','le', 'mano','meni','me', 'med', 'medtem', 'mene', 'mi', 'midva', 'midve', 'mnogo', 'moje', 'moj','moja','mojih','mojemu','moji',
                          'mojima','mojega',"moj'ga",'moja','mojim','mu',
                          'na', 'nad', 'naj', 'najina', 'najino', 'naju', 'nas', 'nato', 'naš', 'naša', 'naše', 'ne', 'nedavno',
                          'nek', 'neka', 'nekaj', 'nekatere', 'nekateri', 'nekatero', 'nekdo', 'neke', 'nekega', 'neki', 'nekje',
                          'neko', 'nekoga', 'ni', 'nikamor', 'nikjer', 'nje', 'njega', 'nje', 'njegova', 'njegovo', 'njej', 'njemu',
                          'njen', 'njena', 'njegova', 'njegovih','njegovo','njegovega','njeno', 'nji', 'njih', 'njihov', 'njihova', 'njihovo', 'njiju', 'njim', 'njo', 'njun',
                          'njuna','nobena','nobene','nobeni','nobeno','noben','nobenega','nobenem','nobenemu','nobenih','nobeni',
                          'nobenih','njuno', 'no', 'npr.', 'o', 'ob', 'oba', 'obe', 'oboje', 'od', 'odprt', 'odprta', 'odprti', 
                          'okoli', 'on', 'onadva', 'one', 'oni', 'onidve', 'osem', 'osma', 'osmi', 'osmo', 'oz.', 
                          'pa', 'po', 'pod', 'pogosto', 'poleg', 'poln', 'polna', 'polni', 'polno', 'ponavadi',
                          'ponovno', 'potem', 'povsod', 'pozdravljen', 'pozdravljeni', 'prav', 'prava', 'prave', 'pravi', 'pravo',
                          'pribl.', 'precej', 'pred', 'preko', 'pri', 'približno', 'primer', 'proti', 'prva', 's',
                          'prvi', 'prvo','rajši','raje','rajš','rajše','rall' ,'ravno', 'redko', 'res', 'reč','riten.','riten', 'saj', 'sam', 'sama', 'same', 'sami', 
                          'samo', 'se', 'sebe', 'sebi', 'sedaj', 'sem', 'seveda', 'si', 'sicer', 'skoraj', 'skozi',
                          'smo', 'so', 'spet', 'sreda', 'srednja', 'srednji', 'srednje', 'sta', 'ste', 'stran', 'stvar', 'sva','svoja', 'svoj',
                          'svoje', 'svojim', 'svojih', 'sred', 'sredi','svojo','svoji','svojim','svojima', 'svojega',
                          'šel', 'šla', 'šli','šlo', 'še',
                          'ta', 'tak', 'taka', 'take', 'taki','takrat', 'tako', 'takoj', 'tam', 'te', 'tebe', 'tebi', 'treba',
                          'tega', 'težak', 'težka', 'težki', 'težko', 'ti', 'tista', 'tiste', 'tisti', 'tisto', 'tj.', 
                          'tja', 'to', 'toda', 'torej', 'tu', 'tudi', 'tukaj', 'tvoj', 'tvoja', 'tvoje', 'u', 'v', 
                          'vaju', 'vam', 'vas', 'vaš', 'vaša', 'vaše', 've', 'vedno', 'velik', 'velika', 'veliki', 
                          'veliko', 'vendar', 'ves', 'več', 'vi', 'vidva', 'vii', 'viii', 'vsa', 'vsaj', 'vsak',
                          'vsaka', 'vsakdo', 'vsake', 'vsaki', 'vsakomur', 'vse', 'vsega', 'vsi', 'vso', 'včasih', 
                          'včeraj', 'x', 'z', 'za','zame','zate' ,'zadaj', 'zadnji', 'zakaj', 'zaprta', 'zaprti', 'zaprto', 'zdaj', 'zelo',
                          'zunaj', 'če', 'često', 'čez', 'čigav', 'že', 'vsazga', 'tazga', 'jest', 'jast', 'svojga', 'mojga', 
                          'njenga','cresc','sost','sostenuto', 'riten', 'tempo', 'adagio', 'andante','allegro','piano', 'pianissimo','forte','fortissimo', 'maestoso']

    else:
        sw=stopwords.words(lang_s)

    return sw
