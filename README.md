# godaddyapi

### 1、说明
<pre><code>
将godaddy账号对应该key的值填写到include.py中的KEYDICT
将godaddy账号对应该secret的值填写到include.py中的SECRETDICT
</code></pre>
### 2、要求
<pre><code>
python 2.7
requests

requests包都可以通过pip install 来安装
</code></pre>
### 3、在开发过程中使用虚拟环境来安装
<pre><code>
在第一步中建立一个项目后，进入到项目的目录后执行virtualenv --no-site-packages myvenv
我加了参数--no-site-packages，这样，已经安装到系统Python环境中的所有第三方包都不会复制过来，
这样，我们就得到了一个不带任何第三方包的“干净”的Python运行环境。
virtualenv可以通过pip 来安装
</code></pre>
### 4、godaddyapi 可以查询账号下的单个域名信息和账号下的所有域名信息,并输出到文件。
1、单个域名
python godaddydomain.py -H api.godaddy.com -i your_godaddy_acount -d search_domain -n -s -t -e -N -o test.txt
2、账号下所有域名
python godaddydomain.py -H api.godaddy.com -i your_godaddy_acount -n -s -t -e -N -o test.txt
### 5、还没有完善，将会慢慢完善。
