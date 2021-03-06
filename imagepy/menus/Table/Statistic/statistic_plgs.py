from imagepy.core.engine import Table
import pandas as pd
from imagepy import IPy

class Statistic(Table):
	title = 'Table Statistic'
	note = ['snap', 'only_num', 'row_msk', 'col_msk']

	para = {'axis':'Column', 'sum':True, 'mean':True,'max':False, 
		'min':False,'var':False,'std':False,'skew':False,'kurt':False}
		
	view = [(list, 'axis', ['Row', 'Column'], str, 'axis', ''),
			(bool, 'sum', 'sum'),
			(bool, 'mean', 'mean'),
			(bool, 'max', 'max'),
			(bool, 'min', 'min'),
			(bool, 'var', 'var'),
			(bool, 'std', 'std'),
			(bool, 'skew', 'skew'),
			(bool, 'kurt', 'kurt')]

	def run(self, tps, snap, data, para=None):
		rst, axis = {}, (0,1)[para['axis']=='Row']
		if para['sum']:rst['sum'] = snap.sum(axis=axis)
		if para['mean']:rst['mean'] = snap.mean(axis=axis)
		if para['max']:rst['max'] = snap.max(axis=axis)
		if para['min']:rst['min'] = snap.min(axis=axis)
		if para['var']:rst['var'] = snap.var(axis=axis)
		if para['std']:rst['std'] = snap.std(axis=axis)
		if para['skew']:rst['skew'] = snap.skew(axis=axis)
		if para['kurt']:rst['kurt'] = snap.kurt(axis=axis)
		IPy.show_table(pd.DataFrame(rst), tps.title+'-statistic')

class GroupStatistic(Table):
	title = 'Group Statistic'

	para = {'major':None, 'minor':None, 'sum':True, 'mean':True,'max':False, 
		'min':False,'var':False,'std':False,'skew':False,'kurt':False, 'cn':[]}
		
	view = [('fields', 'cn', 'field to statistic'),
			('field', 'major', 'group by', 'major'),
			('field', 'minor', 'group by', 'key'),
			
			(bool, 'sum', 'sum'),
			(bool, 'mean', 'mean'),
			(bool, 'max', 'max'),
			(bool, 'min', 'min'),
			(bool, 'var', 'var'),
			(bool, 'std', 'std'),
			(bool, 'skew', 'skew')]

	def run(self, tps, snap, data, para=None):
		by = [i for i in [para['major'], para['minor']] if i!='None']
		gp = data.groupby(by)[para['cn']]

		rst = []
		def post(a, fix): 
			a.columns = ['%s-%s'%(i,fix) for i in a.columns]
			return a

		if para['sum']:rst.append(post(gp.sum(), 'sum'))
		if para['mean']:rst.append(post(gp.mean(), 'mean'))
		if para['max']:rst.append(post(gp.max(), 'max'))
		if para['min']:rst.append(post(gp.min(), 'min'))
		if para['var']:rst.append(post(gp.var(), 'var'))
		if para['std']:rst.append(post(gp.std(), 'std'))
		if para['skew']:rst.append(post(gp.skew(), 'skew'))

		IPy.show_table(pd.concat(rst, axis=1), tps.title+'-statistic')

plgs = [Statistic, GroupStatistic]