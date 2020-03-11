import RAPID

norbert = RAPID.RAPID()

norbert.request_rmmp()
norbert.start_RAPID()

resp = norbert.set_speeddata('vSpeed', 50)
print(norbert.get_rapid_variable('vSpeed'))
resp = norbert.set_zonedata('zZone', 'fine')
#norbert.stop_RAPID()