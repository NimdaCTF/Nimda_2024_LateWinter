from random import choice, shuffle
import sys
import hmac
from os import path

PREFIX = "nimda_просто_привет_фром_россия_"
SECRET = b"russia-england-thai-grape-non-quid-agit-salvete"
SALT_SIZE = 12


def get_salt():
    user_id = sys.argv[1]
    return hmac.new(SECRET, str(user_id).encode(), "sha256").hexdigest()[:SALT_SIZE]


DEVANGARI_ALPHA = [chr(x) for x in range(2308, 2340)]
GUDZHARATI_ALPHA = [chr(x) for x in range(2693, 2727) if x not in (2702, 2706)]
THAI_ALPHA = [chr(x) for x in range(3585, 3617)]

TEXT_TEMPLATE = '''{LANGUAGE} язык - это просто.
Сначала надо запомнить, что буква а пишется как {а}.
Еще в этом языке есть несколько букв о.
Одна из них - букв{а} {о}.
{о}н{а} п{о}х{о}ж{а} н{а} чебурек и перев{о}дится к{а}к п{о}дв{а}л.
{о}чень мн{о}г{о} сл{о}в с букв{о}й с. В языке букв{а} с пишется как {с}.
{с}к{о}р{о} ты привыкнешь. Букв{а} п - {п}, р - {р}, {а} т - {т}.
Е{с}ли {т}ы {п}{о}ним{а}ешь {т}{о}, ч{т}{о} тут н{а}{п}и{с}ан{о} - {т}ы чем{п}и{о}н ми{р}{а} п{о} {с}{т}ег{а}н{о}г{р}{а}фии.
Н{о} э{т}{о}г{о} м{а}л{о} и {п}{о}э{т}{о}му букв{а} н - {н}.

nimda_{п}{р}{о}{с}{т}{о}_{п}{р}иве{т}_ф{р}{о}м_{р}{о}{с}{с}ия_{SALT}
'''


def generate():
    if len(sys.argv) < 3:
        print("Usage: generate.py user_id target_dir", file=sys.stderr)
        sys.exit(1)

    target = sys.argv[2]

    alpha = choice([DEVANGARI_ALPHA, GUDZHARATI_ALPHA, THAI_ALPHA])
    lang_name = ''
    if alpha == DEVANGARI_ALPHA:
        lang_name = 'Супчиковый'
    elif alpha == GUDZHARATI_ALPHA:
        lang_name = 'Котиковый'
    elif alpha == THAI_ALPHA:
        lang_name = 'Барсучий'

    shuffle(alpha)

    open(path.join(target, 'result.txt'), 'w', encoding='UTF-8').write(TEXT_TEMPLATE.format(а=alpha.pop(),
                                                                                            о=alpha.pop(),
                                                                                            с=alpha.pop(),
                                                                                            п=alpha.pop(),
                                                                                            р=alpha.pop(),
                                                                                            т=alpha.pop(),
                                                                                            н=alpha.pop(),
                                                                                            LANGUAGE=lang_name,
                                                                                            SALT=get_salt()
                                                                                            ))


if __name__ == '__main__':
    generate()
