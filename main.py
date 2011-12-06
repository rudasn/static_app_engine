#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os, sys, re
from google.appengine.api import mail
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util, template

APP_NAME = 'APPLICATION NAME'

CONTACT = {
	'owner': 'owner_mail@example.com',
	'admin': 'admin_mail@example.com'
}

class Base(webapp.RequestHandler):
	def get(self):
		return url_handler(self)


def main():
	util.run_wsgi_app(application)


def url_handler(req):
	#	'clean' path
		url = '/'.join([i for i in req.request.path.split('/')[1:] if len(i)])
	
	#	get template name and physical path location
		template_name = u'%s' % (url if url else 'home')
		
		if not url.endswith('.html'):
			template_name = u'%s.html' % template_name
		
		template_file = get_path(file=template_name)
		template_data = {
			'url': url
			, 'template': template_name
			, 'template_file': template_file
			, 'contact': CONTACT
		}
	
	#	render template file according to url
		try:
			out = template.render(template_file, template_data, debug=False)
	
	#	catch and display errors
		except:
			template_name = error_handler(sys.exc_info()[0].__name__, req)
			out = template.render( u'%s.html' % get_path(file=template_name), template_data, debug=False)
	
	#	return the results
		req.response.out.write(out)


def error_handler(error, req):
	mail_me = CONTACT['admin']
	
	if error is 'TemplateDoesNotExist':
		status = 404
		subject = 'Page not found'
	else:
		status = 500
		subject = 'Server error'
	
	body = 'An error occured in "%s"' % req.request.path

#	Send email
	mail.send_mail(mail_me, mail_me, u'[GAE ERROR] %s: %s' % (APP_NAME, subject), body)

#	Set request headers
	req.response.set_status(status,subject)

#	Return status (status must be a template name)
	return status



def get_path(to='templates', file=False):
	path = os.path.join(os.path.dirname(__file__), to)
	if file:
		return u'%s/%s' % (path, file)
	else:
		return path


application = webapp.WSGIApplication([('.*', Base)], debug=True)

if __name__ == '__main__':
	main()
