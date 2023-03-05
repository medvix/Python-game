def sticks(inventory):
    if inventory['wood'] >= 2:
        inventory['wood'] -= 2
        inventory['sticks'] += 4
        return True
    else:
        return False


def axe(inventory):
    if inventory['sticks'] >= 2 and inventory['stone'] >= 3 and inventory['axe'] == 0:
        inventory['sticks'] -= 2
        inventory['stone'] -= 3
        inventory['axe'] += 1
        return True
    else:
        return False


def pickaxe(inventory):
    if inventory['sticks'] >= 2 and inventory['stone'] >= 3 and inventory['pickaxe'] == 0:
        inventory['sticks'] -= 2
        inventory['stone'] -= 3
        inventory['pickaxe'] += 1
        return True
    else:
        return False

