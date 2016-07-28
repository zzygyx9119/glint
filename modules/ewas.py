from utils import LinearRegression #, plot
from numpy import column_stack, ones, savetxt, array
from module import Module
from utils import common, plot
import logging

"""
copy meth_data in advance
"""
class EWAS(Module):
    AVALIABLE_TESTS = ['linear_regression', 'logistic_regression']
    TEST_FUNC_NAME_FORMAT = "_{test_name}_test"   # feature selections function name format

    def __init__(self, methylation_data, tests_list):
        self.meth_data = methylation_data
        self.test_handlers = self._get_test_handler(tests_list)

    def run(self):
        logging.info('starting EWAS...');
        #running association tests
        results = [test_handler(output_filename = 'ewas_' + test_name) for (test_name,test_handler) in self.test_handlers]
        logging.info('EWAS is Done!')
        return results

    def _get_test_handler(self, tests_list):
        # check that the tests in test_list are all optional tests (found in AVALIABLE_TESTS)
        if set(set(tests_list).difference(set(self.AVALIABLE_TESTS))) == 0:
            common.terminate('tests %s are not available' % str(set(tests_list).difference(set(self.AVALIABLE_TESTS))))

        return [(test,getattr(self, self.TEST_FUNC_NAME_FORMAT.format(test_name=test))) for test in tests_list]

    def _logistic_regression_test(self, output_filename = None):
        logging.warning("logistic regression is not supported for the moment...") #todo when implementing remove this
        pass
        
    def _linear_regression_test(self, output_filename = None):
        """
        linear regression test
        """
        logging.info("running linear regression test...")
        output = []
            
        for i, site in enumerate(self.meth_data.data):
            coefs, fstats, p_value = LinearRegression.fit_model(self.meth_data.phenotype, site, covars = self.meth_data.covar) #TODO add test
            output.append([self.meth_data.cpgnames[i], p_value[0], fstats[0], coefs[0]  ])

        
        output.sort(key = lambda x: x[1]) # sort output by p-value
        output = array(output)

        if output_filename:
            qqplot_out = output_filename + '_qqplot' # TODO Elior, change this name (qqplot output file name)?
            logging.info("savings results to %s and qq-plot to %s" % (output_filename, qqplot_out))  
            savetxt(output_filename, output, fmt='%s')
            # plot the p-value
            qqplot = plot.QQPlot(save_file = qqplot_out)
            qqplot.draw(output[:,1].astype(float), title = "TODO Elior, CHANGE THIS", xtitle="TODO Elior, change this x", ytitle = "TODO Elior, change this y")

        return output

