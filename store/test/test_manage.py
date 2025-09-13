# from django.core.management import call_command
# import sys
# from io import StringIO


# def test_manage_py_help_command():
#     """Ensure manage.py runs successfully with 'help' command"""
#     out = StringIO()
#     sys.argv = ['manage.py', 'help']
#     try:
#         call_command('help', stdout=out)
#     except SystemExit:
#         pass
#     assert 'Type \'manage.py help <subcommand>\'' in out.getvalue()
