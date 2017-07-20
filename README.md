# A simple Python implementation for Qiwi Api

# Installation

```
$ pip install pyqiwiapi
```

# Usage

```
from pyqiwiapi import Qiwi

login = 'qiwi-login'
password = 'qiwi-password'
qiwi = Qiwi(login, password)
qiwi.get_tgt_ticket() # Get tgt Qiwi ticket
qiwi.get_st_ticket() # Get st Qiwi ticket
res = qiwi.get_payment_history({'rows': 1}) # Get payment history
print(res)
```
