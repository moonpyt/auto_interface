# for trans in ["daily", "monthly"]:
# for fx in ["daily", "monthly"]:
#     trans_data = ["accumulation", "single"]
#     fx_data = ["accumulation", "single"]
#     if trans == "daily":
#         trans_data = ["single"]
#     if fx == "daily":
#         fx_data = ["single"]
#     for tran_collect in trans_data:
#         for fx_collect in fx_data:
#             print(trans, fx, tran_collect, fx_collect)

# evonet_mop_param
# daily daily single single
# daily monthly single accumulation
# daily monthly single single
# monthly daily accumulation single
# monthly daily single single
# monthly monthly accumulation accumulation
# monthly monthly accumulation single
# monthly monthly single accumulation
# monthly monthly single single

#  position=0
# acquirer_iin = line[0:11]
# forwarding_iin = line[12:23]
# trace_num = line[24:30]
# trans_datetime = line[31:41]
# account_number = line[42:61]  # 未保存
# trans_amount = line[62:74]
# processing_code = line[80:86]
# mcc = line[87:91]
# terminal_number = line[92:100]
# store_id = line[101:116]
# store_english_name = line[117:157]
# retrieval_reference_number = line[158:170]
# service_code = line[171:173]
# authorization_code = line[174:180]
# trans_currency = line[203:206]
# settle_currency = line[211:214]
# settle_amount = line[215:227]
# upi_settle_date = line[237:241]
# fee_receivable = line[273:285]
# fee_payable = line[286:298]

# m = "4444444,ADVICE_TYPE,ADVICE_ID,TRANSACTION_ID,ACCOUNT_NAME,CCY_PAIR,RELATED_ADVICE_ID,SIDE,TRANSACTION_CURRENCY,CONSUMER_CURRENCY,TRANSACTION_CURRENCY_TYPE,AMOUNT,TRANSACTION_TYPE,SCENARIO,SETTLEMENT_AMOUNT,SETTLEMENT_CURRENCY,PAYMENT_PROVIDER,TRANSACTION_TIMESTAMP,REQUESTED_PRICING_REF_ID,CLIENT_REF,ACTUAL_PRICING_REF_ID,PRICE,CONTRA_AMOUNT,VALUE_DATE,MDAQ_PRICE,CONTRA_AMOUNT_MRATE,PROFIT_CCY,PROFIT_AMOUNT,FIXING_ADJUSTMENT,STATUS,ERROR_CODE,ERROR_REASON,PROCESS_TIMESTAMP,RECEIVE_TIMESTAMP,PROFIT_VALUE_DATE,M_VALUE_DATE,VALID_TIMESTAMP,ORIGINAL_PROFIT_AMOUNT,BENEFICIARY_ALIAS,DERIVED_TRANSACTION_TYPE,SERVICE_FEE"
# print(m.lower())


# batch_id,advice_type,advice_id,transaction_id,account_name,ccy_pair,related_advice_id,side,transaction_currency,consumer_currency,transaction_currency_type,amount,transaction_type,scenario,settlement_amount,settlement_currency,payment_provider,transaction_timestamp,requested_pricing_ref_id,client_ref,actual_pricing_ref_id,price,contra_amount,value_date,mdaq_price,contra_amount_mrate,profit_ccy,profit_amount,fixing_adjustment,status,error_code,error_reason,process_timestamp,receive_timestamp,profit_value_date,m_value_date,valid_timestamp,original_profit_amount,beneficiary_alias,derived_transaction_type,service_fee=m.split(",")
# print(batch_id)
# n=[batch_id,advice_type,advice_id,transaction_id,account_name,ccy_pair,related_advice_id,side,transaction_currency,consumer_currency,transaction_currency_type,amount,transaction_type,scenario,settlement_amount,settlement_currency,payment_provider,transaction_timestamp,requested_pricing_ref_id,client_ref,actual_pricing_ref_id,price,contra_amount,value_date,mdaq_price,contra_amount_mrate,profit_ccy,profit_amount,fixing_adjustment,status,error_code,error_reason,process_timestamp,receive_timestamp,profit_value_date,m_value_date,valid_timestamp,original_profit_amount,beneficiary_alias,derived_transaction_type,service_fee]
# for i in n:
#     print("assert data['batchId']==%s" % i.lower())



# for i in m.lower().split(','):

# print(str(n).replace("'",""))

#
# s="batch_id, advice_type, advice_id, transaction_id, related_advice_id, account_name, ccy_pair, side, \
#                 transaction_currency, consumer_currency, transaction_currency_type, amount, transaction_type, \
#                 scenario, settlement_amount, settlement_currency, payment_provider, transaction_timestamp, \
#                 requested_pricing_ref_id, beneficiary, beneficiary_alias, client_ref, status, actual_pricing_ref_id, \
#                 price, contra_amount, value_date, m_value_date, mdaq_rate, mdaq_price, contra_amount_mrate, profit_ccy, \
#                 profit_amount, original_profit_amount, profit_value_date, fixing_adjustment, fxg_adj_client_profit, \
#                 original_batch_id, error_code, error_reason, process_timestamp, receive_timestamp, valid_timestamp, \
#                 derived_transaction_type, service_fee, evonet_order_number, orig_evonet_order_number, settle_date, \
#                 expect_value_date, recon_flag, advice_time, create_time"
# s.split(",").sort()
# for m in s.split(",").sort():
#     print(m.strip())

# m='"EVONET Order Create Time","WOP User Pay Time","MOP Transaction Time","EVONET Order Number","WOP Order Number","MOP Order Number","WOP ID","WOP Name","Transaction Result","Transaction Amount","Transaction Currency","Settlement Amount","Settlement Currency","Original EVONET Order Number"'
# print(m.lower().replace(" ","_").replace('"',''))
# if orig_curency == "SGD" and dst_currency == "JPY":
#     ask = 82.82
#     bid = 79.88
# elif orig_curency == "JPY" and dst_currency == "SGD":
#     ask = 0.01222
#     bid = 0.0101
# elif orig_curency == "SGD" and dst_currency == "USD":
#     ask = 0.754
#     bid = 0.748
# elif orig_curency == "USD" and dst_currency == "JPY":
#     ask = 109
#     bid = 106
#
# elif orig_curency == "JPY" and dst_currency == "USD":
#     ask = 0.0094
#     bid = 0.009
#
# elif orig_curency == "USD" and dst_currency == "SGD":
#     ask = 1.34
#     bid = 1.32
#
# mid = (ask + bid) / 2
# return ask, mid, bid

m={"a":2222222,"b":333333}

n={"a":2222222,"b":999999999333333,"c":"skdflas","data":""}
data=m.update(n)
print(m)

if n.get("data"):
    print(23333333)
