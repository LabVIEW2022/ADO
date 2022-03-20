import time
from ADO import ado

class ID:
    def __init__(self):
        pass
    def scan(self, badge):
        ids = {'16146249080728735934': 'Rin',
                '65092': 'Keith',
                '16146249080728756913': 'Jeff',
                '16146249080728735922': 'Eddie',
                '16146249080728813158': 'Branny',
                '16146249080728814643': 'Will',
                '897550856': 'Test',
                '16146249080728326793': 'Jimmy',
                '16146249080728769947': 'Louie'
                }
        try:
                self.employee = ids[badge]
                print(self.employee)
                ado.GDisplay('Welcome', self.employee, '', '')
                time.sleep(2)
        except KeyError:
                print('User Not Found')
                ado.GDisplay('User', 'Invalid', '', '')
                self.employee = ('Invalid')
                time.sleep(2)
        return self.employee


id = ID()


