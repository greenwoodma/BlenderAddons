# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8-80 compliant>

import bpy
import csv

from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, FloatProperty
from bpy.types import Operator

bl_info = {
    "name": "ESRI ASCII Format (.asc)",
    "author": "Mark A. Greenwood",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "File > Import > ESRI ASCII (.asc) ",
    "description": "Import ESRI ASCII Meshes",
    "warning": "",
    "support": "COMMUNITY",
    "category": "Import-Export",
}


def read_file(context, filepath, scale):
    print("loading ESRI ASCII mesh...")

    def getval(i): return next(i).split()[1]

    objName = bpy.path.display_name_from_filepath(filepath)

    verts = []
    faces = []

    with open(filepath, "r") as ofile:
        ncols = int(getval(ofile))
        nrows = int(getval(ofile))
        xllcorner = float(getval(ofile))
        yllcorner = float(getval(ofile))
        cellsize = float(getval(ofile))

        offset = ofile.tell()
        NODATA_value = ofile.readline().split()
        if NODATA_value[0] == "NODATA_value":
            NODATA_value = NODATA_value[1]
        else:
            print("Assuming NODATA_value of -9999")
            NODATA_value = "-9999"
            ofile.seek(offset)

        print(ncols, nrows, xllcorner, yllcorner, cellsize, NODATA_value)

        asc_reader = csv.reader(ofile, skipinitialspace=True, delimiter=' ')

        for i, row in enumerate(asc_reader):
            if i >= nrows:
                break
            for j in range(int(ncols)):
                if j >= ncols:
                    break
                datum = 0 if (row[j] == NODATA_value) else row[j]
                z = float(datum)
                x = j * cellsize
                y = (nrows-i) * cellsize
                verts.append((x, y, z))

        print('done')
        print('last vertex:', verts[-1])

    # generate_edges, i = verts y, j = verts x
    total_range = ((nrows-1) * (ncols))

    for i in range(total_range):
        if not ((i+1) % ncols == 0):
            faces.append([i, i+ncols, i+ncols+1, i+1])

    # create the mesh from the points
    mesh_data = bpy.data.meshes.new(objName)
    mesh_data.from_pydata(verts, [], faces)
    mesh_data.update()

    # create an object from the mesh
    ascObj = bpy.data.objects.new(objName, mesh_data)

    # add the object into the scene and select it
    scene = context.window.scene
    scene.collection.objects.link(ascObj)
    ascObj.select_set(True)
    context.view_layer.objects.active = ascObj

    # scale the object down to something sensible
    context.view_layer.objects.active.scale = (scale, scale, scale)


class ImportASC(Operator, ImportHelper):
    """Imports ESRI ASCII (.asc) format mesh"""
    bl_idname = "import_mesh.asc"
    bl_label = "Import ESRI ASCII (*.asc)"

    filename_ext = ".asc"

    filter_glob = StringProperty(
            default="*.asc",
            options={'HIDDEN'}
            )

    # scale defaults to 0.01 so that a 1km LIDAR grid square comes out
    # as a more manageable 10x10 mesh when loaded into blender
    scale = FloatProperty(
            name="Scale",
            description="Scale the mesh by this value",
            soft_min=0.0001, soft_max=1000.0,
            min=1e-6, max=1e6,
            default=0.01,
            )

    def execute(self, context):
        read_file(context, self.filepath, self.scale)
        return {'FINISHED'}


def menu_func_import(self, context):
    self.layout.operator(ImportASC.bl_idname, text="ESRI ASCII (.asc)")


def register():
    bpy.utils.register_class(ImportASC)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ImportASC)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()
