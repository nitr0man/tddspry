import os

from datetime import datetime
from random import choice
from string import digits, letters

from twill.commands import get_browser, show
from twill.errors import TwillAssertionError


__all__ = ('show_on_error', )


def show_on_error(func):
    """
    On ``TwillAssertionError``, show last page got by twill.

    By sets up ``TWILL_ERROR_DIR`` environment var all error pages would be
    saved on it.
    """
    def test_wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except TwillAssertionError:
            saved, showed = False, False

            if 'TWILL_ERROR_DIR' in os.environ:
                dirname = os.environ['TWILL_ERROR_DIR']

                if not os.path.isdir(dirname):
                    try:
                        os.mkdir(dirname)
                    except:
                        print 'Cannot create directory at %r.' % dirname
                        show()

                        showed = True

                if not showed:
                    random = \
                        ''.join([choice(letters + digits) for i in range(8)])

                    filename = '%s-%s.html' % (func.__name__, random)
                    filename = os.path.join(dirname, filename)

                    try:
                        file = open(filename, 'w')
                        file.write(get_browser().get_html())
                        file.close()
                    except:
                        print 'Cannot write to file at %r.' % filename
                        show()

                        showed = True
                    else:
                        print 'Output saved to %r.' % filename
                        saved = True

            if not saved and not showed:
                show()

            raise

    test_wrapper.__name__ = func.__name__
    test_wrapper.__doc__ = func.__doc__
    test_wrapper.__dict__.update(func.__dict__)

    return test_wrapper