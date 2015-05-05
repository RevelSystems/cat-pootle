#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) Pootle contributors.
#
# This file is a part of the Pootle project. It is distributed under the GPL3
# or later license. See the LICENSE file for a copy of the license and the
# AUTHORS file for copyright and authorship information.

from django.utils.translation import ugettext_lazy as _

from virtualfolder.models import VirtualFolder


HEADING_CHOICES = [
    {
        'id': 'name',
        'class': 'stats',
        'display_name': _("Name"),
    },
    {
        'id': 'priority',
        'class': 'stats-number sorttable_numeric',
        'display_name': _("Priority"),
    },
    {
        'id': 'project',
        'class': 'stats',
        'display_name': _("Project"),
    },
    {
        'id': 'language',
        'class': 'stats',
        'display_name': _("Language"),
    },
    {
        'id': 'progress',
        'class': 'stats',
        # Translators: noun. The graphical representation of translation status
        'display_name': _("Progress"),
    },
    {
        'id': 'total',
        'class': 'stats-number sorttable_numeric when-loaded',
        # Translators: Heading representing the total number of words of a file
        # or directory
        'display_name': _("Total"),
    },
    {
        'id': 'last-updated',
        'class': 'stats sorttable_numeric when-loaded',
        'display_name': _("Last updated"),
    },
    {
        'id': 'need-translation',
        'class': 'stats-number sorttable_numeric when-loaded',
        'display_name': _("Need Translation"),
    },
    {
        'id': 'suggestions',
        'class': 'stats-number sorttable_numeric when-loaded',
        # Translators: The number of suggestions pending review
        'display_name': _("Suggestions"),
    },
    {
        'id': 'critical',
        'class': 'stats-number sorttable_numeric when-loaded',
        'display_name': _("Critical"),
    },
    {
        'id': 'activity',
        'class': 'stats sorttable_numeric when-loaded',
        'display_name': _("Last Activity"),
    },
]


def get_table_headings(choices):
    """Filters the list of available table headings to the given `choices`."""
    return filter(lambda x: x['id'] in choices, HEADING_CHOICES)


def make_generic_item(path_obj, **kwargs):
    """Template variables for each row in the table."""
    return {
        'href': path_obj.get_absolute_url(),
        'href_all': path_obj.get_translate_url(),
        'href_todo': path_obj.get_translate_url(state='incomplete', **kwargs),
        'href_sugg': path_obj.get_translate_url(state='suggestions', **kwargs),
        'href_critical': path_obj.get_critical_url(**kwargs),
        'title': path_obj.name,
        'code': path_obj.code,
        'is_disabled': getattr(path_obj, 'disabled', False),
    }


def make_directory_item(directory):
    filters = {}

    if VirtualFolder.get_matching_for(directory.pootle_path).count():
        # The directory has virtual folders, so append priority sorting to URL.
        filters['sort'] = 'priority'

    item = make_generic_item(directory, **filters)
    item.update({
        'icon': 'folder',
    })
    return item


def make_store_item(store):
    item = make_generic_item(store)
    item.update({
        'icon': 'file',
    })
    return item


def get_parent(directory):
    parent_dir = directory.parent

    if not (parent_dir.is_language() or parent_dir.is_project()):
        return {
            'icon': 'folder-parent',
            'title': _("Back to parent folder"),
            'href': parent_dir.get_absolute_url()
        }
    else:
        return None


def make_project_item(translation_project):
    item = make_generic_item(translation_project)
    item.update({
        'icon': 'project',
        'title': translation_project.project.name,
    })
    return item


def make_language_item(translation_project):
    item = make_generic_item(translation_project)
    item.update({
        'icon': 'language',
        'title': translation_project.language.name,
    })
    return item


def make_xlanguage_item(resource_obj):
    translation_project = resource_obj.translation_project
    item = make_generic_item(resource_obj)
    item.update({
        'icon': 'language',
        'code': translation_project.language.code,
        'title': translation_project.language.name,
    })
    return item


def make_project_list_item(project):
    item = make_generic_item(project)
    item.update({
        'icon': 'project',
        'title': project.fullname,
    })
    return item


def get_children(directory):
    """Returns a list of children directories and stores for this
    ``directory``.

    The elements of the list are dictionaries which keys are populated after
    in the templates.
    """
    directories = [make_directory_item(child_dir)
                   for child_dir in directory.child_dirs.live().iterator()]

    stores = [make_store_item(child_store)
              for child_store in directory.child_stores.live().iterator()]

    return directories + stores


def make_vfolder_item(virtual_folder, pootle_path):
    return {
        'href_all': virtual_folder.get_translate_url(pootle_path),
        'href_todo': virtual_folder.get_translate_url(pootle_path,
                                                      state='incomplete'),
        'href_sugg': virtual_folder.get_translate_url(pootle_path,
                                                      state='suggestions'),
        'href_critical': virtual_folder.get_critical_url(pootle_path),
        'title': virtual_folder.name,
        'code': virtual_folder.code,
        'priority': virtual_folder.priority,
        'icon': 'folder',
    }


def get_vfolders(directory):
    """Return a list of virtual folders for this ``directory``.

    The elements of the list are dictionaries which keys are populated after
    in the templates.
    """
    return [make_vfolder_item(vf, directory.pootle_path)
            for vf in VirtualFolder.get_visible_for(directory.pootle_path)]
