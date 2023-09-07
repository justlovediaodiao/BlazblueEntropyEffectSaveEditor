# Blazeblue Entropy Effect Save Editor

It's stil in progress. Currently I am able to unpack save file, but I am not yet clear about each field meaning in save file.

## Unpack save file

- Decompress

Game saves are in `~/AppData/LocalLow/91Act/BlazBlueEntropyEffect/Save/`. The filename of save file is a number. The number indicates the sequence of save. 
Save file is compressed by lz4 algorithm. Use [lz4 command line tool](https://github.com/lz4/lz4/releases) to decompress save file:

```
lz4 -d 1 1d
```

- Deserialize

Decompressed file content is serialized by protobuf. Without the original message definition file, I can only attempt to deserialize. Run:

```
python pb.py 1d
```
After deserialization, you can get a set of field values, but without field names.

- Compress

After you have made modifications to the save file, You should compress it. Save file compressed by lz4 command line tool is not recognized by the game. You need to run following command to compress:

```
python lz4.py 1d 1
```
This is likely due to the version incompatibility of lz4. The command above uses a `lz4.dll` version obtained from the game developer's project [lz4-unity](https://github.com/91Act/lz4-unity).


## Modify save file

Game files are in `Steam/steamapps/common/BlazblueEntropyEffect`. Use [Il2CppDumper](https://github.com/Perfare/Il2CppDumper/releases) to decompile game file.

```
mkdir dll
Il2CppDumper GameAssembly.dll global-metadata.dat dll
```

`global-metadata.dat` is in `BlazblueEntropyEffect_Data/il2cpp_data/Metadata/`.
After decompilation, you can get a set of DLLs that contain types information but do not include source code. You can use [ILSpy](https://github.com/icsharpcode/ILSpy/releases) to see DLLs.
Protobuf definition of the save file can be found in the the DLLs. The work is still in progress.

Another approach is to compare two save files to identify the differences and infer the meaning of the fields based on those differences.
