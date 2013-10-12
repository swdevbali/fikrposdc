from setuptools import setup

setup(name='Fikr POS DC',
      version='1.0',
      description='Centralized and distributed POS report',
      author='Eko Wibowo',
      author_email='swdev.bali@gmail.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=
      [
        'Flask==0.10.1', 
        'MarkupSafe',
        'Flask-SQLAlchemy==1.0',
        'simplejson==3.3.0',
        'flask-classy==0.6.3',
        'Flask-Login==0.2.7',
        'Flask-WTF==0.9.2',
        'Flask-REST==1.1'
       ],
     )
