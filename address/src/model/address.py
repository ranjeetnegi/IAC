class Address:
    def __init__(self, address, state, district, block, pin, phone):
        self.address = address
        self.state = state
        self.district = district
        self.block = block
        self.pin = pin
        self.phone = phone
    
    def __lt__(self, other):
        val1, val2 = self.__evaluate(other)
        if val1 < val2:
            return True
        else:
            return False

    def __evaluate(self, other):
        val1 = len(self.address)
        val2 = len(other.address)
        return val1, val2
    
    def print_attributes(self):
        data = ""
        if self.state != None:
            data = data + " State:" + self.state
        if self.district != None:
            data = data + ",District:" + self.district
        if self.block != None:
            data = data + ",Block:"+ self.block
        if self.pin != None:
            data = data +",Pin:" + self.pin
        if self.phone != None:
            data = data +",Phone:" + self.phone
        if self.address != None:
            data = data +" Address:" + self.address
        print(data)
    
    def capitalize_address(self):
        address_tokens = self.address.split(" ")
        capital_word_array = []
        for address_token in address_tokens:
            if len(address_token.strip()) > 0:
                capital_word_array.append(address_token.strip().capitalize())
        self.address = " ".join(capital_word_array)