# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.downloadwizard.download_tool import  download_all_model_by_url

class DownloadAllModel(http.Controller):
    @http.route('/web/binary/download_model',type='http', auth="public")
    def download_all_model_controller(self,download_model=None,download_model_id = None, active_domain=None, download_key= None, **kw):
        response = download_all_model_by_url(download_model=download_model,download_model_id = download_model_id, active_domain=active_domain, download_key= download_key)
        return response
