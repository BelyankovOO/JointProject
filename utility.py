
'''
cooldown_tick(cooldowns, delta, callbacks={})
cooldowns - словарь {имя : текущее время}
delta - текущая разница во времени (то, что надо отнять от всех КД)
callbacks - словарь {имя : функция}, вызвать функцию, если соответствующий таймер стал равным 0
'''
def cooldown_tick(cooldowns, delta, callbacks={}):
	for name in cooldowns:
		if cooldowns[name] > 0:
			cooldowns[name] -= delta
			if cooldowns[name] <= 0:
				cooldowns[name] = 0
				if name in callbacks:
					callbacks[name]()
			