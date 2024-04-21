import senfenico

senfenico.api_key = 'sk_test_cf59018e-45af-41ea-b28a-5fb122636e00'


#SETTLEMENT
settlement = senfenico.Settlement.create(1000)
print('settlement created...')
print(settlement)

settlement = senfenico.Settlement.list()
print(settlement)

"""
#CHECKOUT
init = senfenico.Checkout.initialize(100, 'http://website.com/success', 'http://www.website.com/cancel')
print(init)
co = senfenico.Checkout.fetch("655342d1-c1a3-44eb-aee7-a2fddcadeaf2")
print(co)
checkout_list = senfenico.Checkout.list()
print(checkout_list)


#CHARGE
charge = senfenico.Charge.create(2000, '65000000', 'orange_bf')
print(charge)
otp_submission = senfenico.Charge.submit_otp("123456", "d426fe9b-01e3-4f76-aac5-d873a07108a9")
print(otp_submission)
charge_list = senfenico.Charge.list()
print(charge_list)


#BALANCE
balance = senfenico.Balance.fetch()
print(balance)
"""
