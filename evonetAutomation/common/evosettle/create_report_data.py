import random
import time
from common.evosettle.comm_funcs import CommonName


class CreateReportData(object):

    def __init__(self):
        self.common_name = CommonName()

    def return_int_str(self, length):
        start = int(str(1).ljust(length, "0"))
        last = int(str(9).ljust(length, "0"))
        return str(random.randint(start, last))

    def random_char(self, length):
        words = ''
        for i in range(length):
            words += chr(random.randint(97, 122))
        return words

    def upi_fee_data(self, file_name):
        upi_fee_data = []
        for trans_code in ["E20", "E30"]:
            for amount_start in ["C", "D"]:
                settle_currency = "392"
                if amount_start == "C":
                    settle_currency = "156"
                amount = str(random.randint(320714, 920714))
                reason_code = str(random.randint(1000, 9000))
                sender1 = str(random.randint(10000000000, 90000000000))
                sender2 = str(random.randint(10000000000, 90000000000))
                receiver1 = str(random.randint(10000000000, 90000000000))
                receiver2 = str(random.randint(10000000000, 90000000000))
                trans_date_time = str(random.randint(1000000000, 9000000000))
                trace_num = str(random.randint(320714, 920714))

                upi_data = trans_code + " " + amount_start + "000000" + amount + " " + reason_code + " " + sender1 + " " + sender2 + " " + receiver1 + " " + receiver2 + " " + trans_date_time + " " + trace_num + "                     " + settle_currency + "                                                                                                                                                                                                     "
                upi_data = upi_data.ljust(309) + "\n"
                upi_fee_data.append(upi_data)
        with open(file_name, "w") as upi_file:
            for line in upi_fee_data:
                upi_file.write(line)

    def icom_detail_data(self, file_name):
        upi_icom_data = []
        for message_type in ["0200 ", "0220 ", '0422 ']:
            if message_type == "0200 ":
                process_codes = ["00x000 ", "01x000 ", "24x000 "]
            elif message_type == "0220 ":
                process_codes = ["00x000 ", "22x000 ", "02x000 ",
                                 "29x000 ", "20x000 ", "19x000 "]
            elif message_type == "0422 ":
                process_codes = ["22x000 ", "02x000 "]
            for processing_code in process_codes:
                acquirer_iin = self.return_int_str(11) + " "
                forwarding_iin = self.return_int_str(11) + " "
                trace_num = self.return_int_str(6) + " "
                trans_datetime = self.return_int_str(10) + " "
                account_number = self.return_int_str(19) + " "
                trans_amount = self.return_int_str(12) + " "
                # message_type = self.return_int_str(4) + " "
                # processing_code = self.return_int_str(6) + " "  # 87
                serviceCode = self.return_int_str(2) + " "
                author_ization_code = self.return_int_str(6) + " "
                trans_currency = "156 "
                settle_currency = "156 "
                if message_type == "0422 ":
                    trans_currency = "392 "
                    settle_currency = "392 "
                settle_amount = self.return_int_str(12) + " "
                fee_receivable = random.choice([self.return_int_str(12) + " ", "000000000000 "])
                fee_payable = random.choice([self.return_int_str(12) + " ", "000000000000 "])
                upi_data = acquirer_iin + forwarding_iin + trace_num + trans_datetime + account_number + trans_amount + message_type + processing_code + "7011 12345678 123456789012345 CHN29000CHINA UNIONPAY SIMULATOR         000000144513 " + serviceCode + author_ization_code + "42910392    000000 00 " + trans_currency + "042 " + settle_currency + settle_amount + "64933299 0104 1230 156 000000000049 64933299 " + fee_receivable + fee_payable + "D00000000000     00000000 D00000000000 156 30001000      1 70200          00300F                                                                                                                                 00 01 6292603466594327    1"
                upi_data = upi_data.ljust(681) + "\n"
                upi_icom_data.append(upi_data)
        with open(file_name, "w") as upi_file:
            for line in upi_icom_data:
                upi_file.write(line)

    def create_ierrn_file_content(self, processing_code, service_code):
        data = ""
        for currency_code in ["156", "392"]:
            time.sleep(2)
            trans_currency = currency_code
            settle_currency = currency_code
            fee_payable = self.return_int_str(12)
            fee_receivable = self.return_int_str(12)
            acquirer_iin = self.return_int_str(11)
            trace_num = self.return_int_str(6)
            trans_datetime = time.strftime("%m%d%H%M%S", time.localtime(time.time()))
            message_type = "0220"
            store_id = self.return_int_str(15)
            store_english_name = self.random_char(40)
            mcc = self.return_int_str(4)
            terminal_number = self.return_int_str(8)
            authorization_code = self.return_int_str(6)
            retrieval_reference_number = self.return_int_str(12)
            upi_Settle_date = self.return_int_str(4)
            forwarding_iin = self.return_int_str(8).ljust(11, " ")
            account_number = self.return_int_str(19)
            trans_amount = self.return_int_str(12)
            settle_amount = self.return_int_str(12)
            upi_ierrn = acquirer_iin + " " + forwarding_iin + " " + trace_num + " " + trans_datetime + " " + account_number + " " + trans_amount + " " + message_type + " " + processing_code + " " + mcc + " " + terminal_number + " " + store_id + " " + store_english_name + " " + retrieval_reference_number + " " + service_code + " " + authorization_code + " 42910392    072550 00 " + trans_currency + " 042 " + settle_currency + " " + settle_amount + " 64933299 " + upi_Settle_date + " 1217 156 000000000493 64933299 " + fee_receivable + " " + fee_payable + " D00000000000 D00000000000 1217141124 000000 F     7020100D         29656                                                                  00 01 1"
            upi_data = upi_ierrn.ljust(673) + "\n"
            data += upi_data
        return data

    def upi_ierrn_data(self, file_name):
        upi_ierrn_list = []
        for service_code in ["00", "83"]:
            upi_ierrn_list.append(self.create_ierrn_file_content("220000", service_code))
        charge_back_num = self.return_int_str(6)
        for processing_code in ["020000", charge_back_num]:
            if processing_code == "020000":
                upi_ierrn_list.append(self.create_ierrn_file_content(processing_code, "00"))
                upi_ierrn_list.append(self.create_ierrn_file_content(processing_code, "17"))
            else:
                upi_ierrn_list.append(self.create_ierrn_file_content(charge_back_num, "17"))
        with open(file_name, "w") as upi_file:
            for line in upi_ierrn_list:
                upi_file.write(line)

    def comm_file_data(self, file_name):
        with open(file_name, "w") as comn_file:
            m = "25000344    00020344    855894 0104114123 6229343390000756    000000032800 0200 000000 5972 00000010 100000000000006 Test Merchant            HK          HKG 010488039526 00        42910392    000000 00 344 942 156 000000027690 78442003 0104 1230 156 000000027690 78442003 000000000152 000000000097 D00000000000     00000000 D00000000000 156 30001000      1 34400          00700F                                                                                                                                 00 01 6292603493382662    1                                                                                                                                                  " + "\n"
            comn_file.write(m)
            n = "25000344    00020344    425752 0104111939 6229343390000756    000000010000 0200 000000 5972 00000010 100000000000006 Test Merchant            HK          HKG 010433858208 00        42910392    000000 00 344 942 156 000000008442 78442003 0104 1230 156 000000008442 78442003 000000000046 000000000030 D00000000000     00000000 D00000000000 156 30001000      1 34400          00700F                                                                                                                                 00 01 6292603493382662    1                                                                                                                                                  " + "\n"
            comn_file.write(n)

    def mdaq_execrpt_file(self, file_name, settle_date):
        # 造mdap file

        with open(file_name, mode='wt', encoding='utf-8') as file:
            file.write(self.common_name.mdap_file_title)  # 写入title
            for i in range(6):
                batch_id = self.random_char(40)
                advice_type = 'EA'
                advice_id = self.return_int_str(20)
                transaction_id = self.return_int_str(20)
                account_name = self.random_char(10)
                ccy_pair = 'SGD/USD'
                related_advice_id = self.return_int_str(20)
                side = random.choice(['BUY', 'SELL'])
                transaction_currency = random.choice(['USD', 'CNY'])
                consumer_currency = random.choice(['USD', 'CNY'])
                transaction_currency_type = 'DELIV'
                amount = random.choice([self.return_int_str(5), str(random.randint(1000, 9000) * 0.001)])
                transaction_type = random.choice(['REFUND', 'SALE'])
                scenario = self.random_char(10)
                settlement_amount = random.choice([self.return_int_str(5), str(random.randint(1000, 9000) * 0.001)])
                settlement_currency = random.choice(['USD', 'CNY'])
                payment_provider = self.random_char(15)
                transaction_timestamp = '2021-04-07 02:41:54.998'
                requested_pricing_ref_id = self.random_char(20)
                client_ref = self.random_char(15)
                actual_pricing_ref_id = self.return_int_str(15)
                price = self.return_int_str(7)
                contra_amount = random.choice([self.return_int_str(5), str(random.randint(1000, 9000) * 0.001)])
                value_date = settle_date[0:4] + "-" + settle_date[4:6] + "-" + settle_date[6:]
                mdaq_price = random.choice([self.return_int_str(7), str(0.568491)])
                contra_amount_mrate = random.choice([self.return_int_str(7), str(33.56)])
                profit_ccy = random.choice(['USD', 'CNY'])
                profit_amount = random.choice([self.return_int_str(7), str(0.568491)])
                fixing_adjustment = self.return_int_str(7)
                status = 'VALID'
                error_code = self.return_int_str(4)
                error_reason = self.random_char(12)
                process_timestamp = '2021-04-07 02:22:54.998'

                receive_timestamp = '2021-04-06 02:41:54.398'
                profit_value_date = '2021-04-' + str(random.randint(11, 28))
                m_value_date = '2021-04-' + str(random.randint(11, 28))
                valid_timestamp = '2021-04-07 06:33:54.998'
                original_profit_amount = random.choice(
                    [self.return_int_str(5), str(random.randint(1000, 9000) * 0.001)])
                beneficiary_alias = self.random_char(10)
                derived_transaction_type = random.choice(["REFUND", "SALE"])
                service_fee = random.choice([self.return_int_str(7), str(0.568491)])
                data = ",".join(
                    [batch_id, advice_type, advice_id, transaction_id, account_name, ccy_pair, related_advice_id, side,
                     transaction_currency, consumer_currency, transaction_currency_type, amount, transaction_type,
                     scenario,
                     settlement_amount, settlement_currency, payment_provider, transaction_timestamp,
                     requested_pricing_ref_id, client_ref, actual_pricing_ref_id, price, contra_amount, value_date,
                     mdaq_price, contra_amount_mrate, profit_ccy, profit_amount, fixing_adjustment, status, error_code,
                     error_reason, process_timestamp, receive_timestamp, profit_value_date, m_value_date,
                     valid_timestamp,
                     original_profit_amount, beneficiary_alias, derived_transaction_type, service_fee]) + "\n"

                file.write(data)


if __name__ == '__main__':
    m = CreateReportData()
    # m.upi_fee_data("20210110")
    m.upi_ierrn_data("fcp")
