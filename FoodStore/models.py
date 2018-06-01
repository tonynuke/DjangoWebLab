from django.db import models


# Create your models here.


class Item(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    price = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()


class CartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def get_price(self):
        return self.quantity * self.item.price


class Cart(models.Model):
    phone = models.CharField(max_length=16)
    items = models.ManyToManyField(CartItem)

    def get_price(self):
        result = sum([i.get_price() for i in self.items.all()])
        return result

    def upsert_item(self, item_id):
        try:
            existing_item = self.items.get(item_id=item_id)
        except:
            existing_item = None

        if existing_item is not None:
            existing_item.quantity = existing_item.quantity + 1
            existing_item.save()
        else:
            new_item = CartItem(item_id=item_id, quantity=1)
            new_item.save()
            self.items.add(new_item)
        self.save()

    def remove_item(self, item_id):
        try:
            existing_item = self.items.get(item_id=item_id)
        except:
            return

        if existing_item.quantity == 1:
            existing_item.delete()
        else:
            existing_item.quantity = existing_item.quantity - 1
            existing_item.save()
        self.save()
