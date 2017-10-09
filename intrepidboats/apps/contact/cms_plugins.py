from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import JobDescriptionPlugin, EmployeeProfilePlugin, CompanyAreaPlugin


class CompanyAreaCMSPlugin(CMSPluginBase):
    model = CompanyAreaPlugin
    name = "Company Area"
    render_template = "contact/company_area.html"
    allow_children = True
    child_classes = ['EmployeeProfileCMSPlugin']
    module = 'Custom'


class EmployeeProfileCMSPlugin(CMSPluginBase):
    name = "Employee Profile"
    model = EmployeeProfilePlugin
    render_template = "contact/employee_profile.html"
    module = 'Custom'


class JobDescriptionCMSPlugin(CMSPluginBase):
    model = JobDescriptionPlugin
    name = "Job Description"
    render_template = "contact/job_description.html"
    cache = False
    module = 'Custom'

plugin_pool.register_plugin(CompanyAreaCMSPlugin)
plugin_pool.register_plugin(EmployeeProfileCMSPlugin)
plugin_pool.register_plugin(JobDescriptionCMSPlugin)
