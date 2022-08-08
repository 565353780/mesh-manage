#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Data.channel_mesh import ChannelMesh

class MeshLoader(object):
    def __init__(self):
        self.channel_mesh = ChannelMesh()
        return

def demo():
    mesh_loader = MeshLoader()
    return True

