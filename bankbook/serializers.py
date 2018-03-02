from allthatbank.utils.cipher import AESCipher
from rest_framework import serializers
from .models import Bankbook


class BankbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bankbook
        fields = '__all__'

    def to_internal_value(self, data):
        # 계좌번호 암호화
        ret = super(BankbookSerializer, self).to_internal_value(data)
        ret['account_number'] = AESCipher().encrypt_str(ret['account_number'])

        return ret

    def to_representation(self, instance):
        # 계좌번호 복호화
        ret = super(BankbookSerializer, self).to_representation(instance)
        ret['account_number'] = AESCipher().decrypt_str(ret['account_number'])

        return ret
