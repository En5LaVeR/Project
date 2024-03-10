class Selection_of_dosage:

    def __init__(self, weight: float):
        self.weight = weight

    def medicines(self):
        self.weight = float(input('Введите вес Собаки (в кг)'))
        return self.ivermektin(), self.alben()

    def ivermektin(self):
        return (
            f"Ивермек = {0.02 * self.weight}мл;\nПроизводитель не рекомендует использовать раствор для инъекций для собак и кошек.\n"
            f"Изначально он предназначался для свиней, лошадей, овец и крупного рогатого скота.")

    def alben(self):
        return f'Alben = {10 * self.weight}мг'


dog1 = Selection_of_dosage(weight=0)
result = dog1.medicines()
for a_drug in result:
    print(a_drug)
