from collections import OrderedDict
from StringIO import StringIO

import numpy as np
from django.core.management.base import BaseCommand, CommandError

from app.models import Submission, Metric
from app.inventories import inventory_by_id, BigFive, CoreSelf, CareerCommitment, Ambiguity, FiroB, Via

numeric_inventories = ('BigFive', 'CoreSelf')

class NumericResult:

    def get_header(self):
        return 'Metric\tMean\tStdev\tMin\tMax'

    def get_row(self):
        if self.has_data:
            nd = 3
            return '{}\t{}\t{}\t{}\t{}'.format(self.key, 
                *np.around((self.mean, self.stdev, self.min, self.max), 3))
        else:
            return '{}\tNO_DATA'.format(self.key)

class Command(BaseCommand):

    help = 'Export mean, stdev, and range data for all inventories'
     
    def handle(self, **options):
        self.setup_data_dict()
            
        for submission in Submission.objects.all():
            metrics = Metric.objects.filter(submission=submission)
        
            inventory_cls = inventory_by_id[submission.inventory_id]
            
            inventory_name = inventory_cls.__name__
            if inventory_name in numeric_inventories:
                self.handle_numeric(inventory_name, metrics)
                
        self.do_calc()
        self.do_write()
                
    def setup_data_dict(self):
        self.data = {}
        
        for inventory_cls in inventory_by_id.values():
            self.data[inventory_cls.__name__] = OrderedDict()         
        
        all_keys = OrderedDict({
            'BigFive': ('extraversion', 'agreeableness', 'conscientiousness',
                'emotional_stability', 'openness'),
            'CoreSelf': ('score',)
        })
        
        for inventory in all_keys:
            for key in all_keys[inventory]:
                self.data[inventory][key] = []
                
    def handle_numeric(self, inventory, metrics):
        for key in self.data[inventory]:
            metric = metrics.filter(key=key)[0]
            self.data[inventory][key].append(metric.value)
           
    def do_calc(self):
        self.result_objs = OrderedDict()
    
        for inventory in numeric_inventories:
            self.result_objs[inventory] = []
        
            for key in self.data[inventory]:
                data = self.data[inventory][key]
            
                result = NumericResult()
                result.key = key
                
                if len(data) == 0:
                    result.has_data = False
                else:  
                    result.has_data = True
                    result.mean = np.mean(data)
                    result.stdev = np.std(data)
                    result.min = min(data)
                    result.max = max(data)
                
        
                self.result_objs[inventory].append(result)
        
    def do_write(self):
        outstream = StringIO()
        
        for inventory in self.result_objs:
            outstream.write('{}\n'.format(inventory))
            outstream.write(self.result_objs[inventory][0].get_header()+'\n')
            
            for result in self.result_objs[inventory]:                
                outstream.write(result.get_row()+'\n')
            
            outstream.write('\n')
            
        print(outstream.getvalue())            
        print('\n')

        outfile_name = 'export_stats.txt'        
        outfile = open(outfile_name, 'w')
        outfile.write(outstream.getvalue())
        print('Wrote results to `{}`.'.format(outfile_name))
