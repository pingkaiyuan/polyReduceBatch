# -*- coding: utf-8 -*-
import pymel.core as pm
import maya.mel as mel
import maya.cmds as cmds
import os
pathInputWindow = pm.promptDialog(title='模型路径设置',message='模型路径:',button=['确认', '取消'],defaultButton='OK',cancelButton='Cancel',dismissString='Cancel')
if pathInputWindow==u'\u786e\u8ba4':
    pathOfFiles = pm.promptDialog(query=True,text=True)
    pathOfFiles=pathOfFiles.replace('\\','/')
    pathOfFiles=pathOfFiles+'/'
reduceInputWindow = pm.promptDialog(title='减面设置',message='减少至（%）:',button=['确认', '取消'],defaultButton='OK',cancelButton='Cancel',dismissString='Cancel')
if pathInputWindow==u'\u786e\u8ba4':
    reducePercent=100-int(pm.promptDialog(query=True,text=True))
files=pm.getFileList(folder=pathOfFiles)
os.mkdir(pathOfFiles+'/ReducedFiles/')
fileCount=len(files)
if len(files)==0:
    cmds.warning('No Files Found')
else:
    for f in files:
        if f!='.DS_Store':
            cmds.file(pathOfFiles+f,i=True)
        else:
            fileCount-=1
    pm.rename('_Mesh','_Mesh0')
    for i in range(1,fileCount):
        pm.rename('_Mesh'+str(fileCount-1-i),'_Mesh'+str(fileCount-i))
    pm.rename('Mesh','_Mesh0')
    startNameInputWindow = pm.promptDialog(title='前缀名设置',message='前缀名:',button=['确认', '无前缀名'],defaultButton='OK',cancelButton='Cancel',dismissString='Cancel')
    if startNameInputWindow==u'\u786e\u8ba4':
        startName=pm.promptDialog(query=True,text=True)
    else:
        startName=''
    endNameInputWindow = pm.promptDialog(title='后缀名设置',message='后缀名:',button=['确认', '无后缀名'],defaultButton='OK',cancelButton='Cancel',dismissString='Cancel')
    if endNameInputWindow==u'\u786e\u8ba4':
        endName=pm.promptDialog(query=True,text=True)
    else:
        endName=''
    startIndexInputWindow = pm.promptDialog(title='起始值设置',message='起始值:',button=['确认', '取消'],defaultButton='OK',cancelButton='Cancel',dismissString='Cancel')
    if startIndexInputWindow==u'\u786e\u8ba4':
        startIndex=pm.promptDialog(query=True,text=True)
    else:
        startIndex='0'
    for j in range(fileCount):
        pm.select('_Mesh'+str(j))
        mel.eval('polyCleanupArgList 4 { "0","1","1","0","0","0","0","0","0","1e-05","0","1e-05","0","1e-05","0","1","0","1" }')
        pm.select('_Mesh'+str(j))
        pm.polyReduce(ver=1,p=reducePercent,n="_Mesh"+str(j))
        indexName='%04d' % (j+int(startIndex))
        pm.exportSelected(pathOfFiles+'/ReducedFiles/'+startName+indexName+endName+'.obj',force=1,options='groups=0;ptgroups=0;materials=0;smoothing=0;normals=0')
