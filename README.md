> 手搓实现了DES和AES算法，并且设置了DES的GUI界面，同时比较了DES和AES的性能以及已有库中的算法的性能，AES确实比DES要快，但是手搓实现的比已有库中的慢很多，手搓实现的逻辑仅供参考

1. `DES.py`中是所有的DES的手搓实现，`DES_GUI.py`中是关于DES的图形化界面
2. `AES.py`中是AES的实现逻辑，但是本算法中把列排序转换成了行排序
3. `test`相关的py文件内部全是开发过程中的测试代码，无所谓
4. `time_compare.py`集成了手搓的和库实现的加密解密的时间方法
5. `time_compare_random.py`集成了随机数据的处理时间的结果的对比
6. `time_compare_gui.py`构造各算法的图形化界面并且展示时间

![image-20241105155219684](C:\Users\zx\Desktop\DOC\grade4up\BDIC3025安全与隐私\DES_AES\assets\image-20241105155219684.png)

> 手搓的AES明显比DES快，但是集成到库中的两个算法的时间相差不大

---

> Manually implemented the DES and AES algorithms, and set up a GUI interface for DES. Additionally, compared the performance of DES and AES with the algorithms in existing libraries. AES is indeed faster than DES, but the manually implemented versions are much slower than those in the existing libraries. The logic of the manual implementations is for reference only.

1. `DES.py` contains the manual implementation of the entire DES algorithm, and `DES_GUI.py` contains the graphical user interface related to DES.
2. `AES.py` contains the implementation logic of AES, but in this algorithm, column sorting has been converted to row sorting.
3. The `test`-related py files are all test codes from the development process and are not important.
4. `time_compare.py` integrates the timing methods for manual and library-implemented encryption and decryption.
5. `time_compare_random.py` integrates the comparison of processing time results for random data.
6. `time_compare_gui.py` constructs the graphical user interface for various algorithms and displays the timing results.

> The manually implemented AES is significantly faster than DES, but the time difference between the two algorithms integrated into the library is not significant.
