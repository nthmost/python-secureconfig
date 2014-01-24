from simplejson import dumps, loads

from baseclass import SecureConfig

class SecureJson(SecureConfig):
    
    def _fill(self, txt):
        self.cfg = loads(txt)

    def _serialize(self):
        return self.to_json()

    def to_json(self):
        return dumps(self.cfg)


if __name__=='__main__':
    
    testjson = """{
    "api": "http://lims.locusdev.net/api/create_combined_picard_data_file_2/",
    "timeout": "500",
    "tsvpath": "/locus/data/picard_metrics/combo_picard_metrics_dbl_wide.tsv",
    "log": "/var/log/shiny/picard_metrics_v2.log"
}"""

    sjson = SecureJson(rawtxt=testjson, keyloc='keys', readonly=False)

    sjson.cfg['tsvpath'] = 'your mom'

    print sjson


