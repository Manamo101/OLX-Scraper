
class Offer:
    def __init__(self, offer_id: str, title: str, price: str, location: str, date: str, ref: str):
        self.offer_id = offer_id
        self.title = title
        self.price = price
        self.location = location
        self.date = date
        self.ref = ref

    def __eq__(self, other):
        if not isinstance(other, Offer):
            return NotImplemented
        return self.offer_id == other.offer_id

    def __hash__(self):
        return hash(self.offer_id)

    def __str__(self):
        return f"Title: {self.title}, Price: {self.price}, Location: {self.location}, Date: {self.date}, Ref: {self.ref}\n"

    def __repr__(self):
        return f"Title: {self.title}, Price: {self.price}, Location: {self.location}, Date: {self.date}, Ref: {self.ref}\n"