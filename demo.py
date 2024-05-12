import senfenico
senfenico.api_key = 'sk_live_3bd5048b-46fb-4b3d-b77f-bca65f93b191'

charge_list = senfenico.Charge.list()
print(charge_list)

"""
#SETTLEMENT
settlement = senfenico.Settlement.create(500)
print(settlement)
settlement = senfenico.Settlement.fetch("655342d1-c1a3-44eb-aee7-a2fddcadeaf2")
print(settlement)
settlement = senfenico.Settlement.list()
print(settlement)
settlement = senfenico.Settlement.cancel("74bba04a-16e0-491d-a991-c4726799f68e")
print(settlement)


#CHECKOUT
init = senfenico.Checkout.initialize(
    amount=100, 
    success_url='http://website.com/success', 
    cancel_url='http://www.website.com/cancel')
print(init)
co = senfenico.Checkout.fetch("655342d1-c1a3-44eb-aee7-a2fddcadeaf2")
print(co)
checkout_list = senfenico.Checkout.list()
print(checkout_list)


#CHARGE
charge = senfenico.Charge.create(amount=2000, phone='65000000', provider='orange_bf')
print(charge)
otp_submission = senfenico.Charge.submit_otp("123456", "d426fe9b-01e3-4f76-aac5-d873a07108a9")
print(otp_submission)
charge = senfenico.Charge.fetch('1c32d1c7-dc81-49c5-85b0-7f6f3498e4a2')
print(charge)
charge_list = senfenico.Charge.list()
print(charge_list)


#BALANCE
balance = senfenico.Balance.fetch()
print(balance)
"""
