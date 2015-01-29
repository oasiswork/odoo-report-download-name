# -*- coding: utf-8 -*-
import pdb
from openerp.addons.web.http import Controller, route, request
from openerp.addons.report.controllers.main import ReportController
from openerp.osv import osv
from openerp import http
import simplejson

class PTReportController(ReportController):
    @route(['/report/download'], type='http', auth="user")
    def report_download(self, data, token):
        requestcontent = simplejson.loads(data)
        url, type = requestcontent[0], requestcontent[1]
        response = ReportController().report_download(data, token)

        if type == 'qweb-pdf':
            reportname = url.split('/report/pdf/')[1].split('?')[0]
            docids = None
            if '/' in reportname:
                reportname, docids = reportname.split('/')

            if docids:
                report_obj = request.registry['report']
                cr, uid, context = request.cr, request.uid, request.context
                report = report_obj._get_report_from_name(cr, uid, reportname)

                if ',' in docids:
                    ids = [int(docids.split(',')[0])]
                else:
                    ids = [int(docids)]

                attachment = report_obj._check_attachment_use(cr, uid, ids, report)
                filename = attachment[ids[0]]

                response.headers.set('Content-Disposition', 'attachment; filename=%s;' % filename)

        return response
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
