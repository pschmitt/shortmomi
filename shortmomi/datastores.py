# coding: utf-8

from __future__ import absolute_import
from pyVmomi import vim
from .tasks import wait_for_tasks


def datastore_search_file(service, datastore, filename):
    details = vim.host.DatastoreBrowser.FileInfo.Details(
        fileType=True, fileSize=True, fileOwner=True, modification=True
    )
    search = vim.host.DatastoreBrowser.SearchSpec(
        sortFoldersFirst=True, details=details, matchPattern=[filename]
    )
    path = f"[{datastore.name}]"
    task = datastore.browser.SearchSubFolders(datastorePath=path, searchSpec=search)
    wait_for_tasks(service, [task])
    results = []
    for r in task.info.result:
        for f in r.file:
            # discard folders
            if r.folderPath == f"[{datastore.name}]":
                continue
            results.append((r.folderPath, f))

    return results
