基于django的微信二维码模块
============================

功能说明：
----------

- 每个微信会员有一个唯一的二维码
- 可以记录用户的来源

快速开始:
---------

安装 *django-wechat-qrcode* :

.. code-block::

    pip install django-wechat-qrcode

修改 *settings.py* 文件:

.. code-block::

    INSTALLED_APPS = (
        ...
        'wechat',
        'wechat_message',
        'wechat_member',
        'wechat_qrcode',
        ...
    )

修改 *urls.py* 文件:

.. code-block::

    url(r'^qrcode/', include('wechat_qrcode.urls')),

更新数据库:

.. code-block::

   python manage.py makemigrations wechat_qrcode 
   python manage.py migrate

微信开发者链接:

    http://yourdomain/qrcode/wx/

用户二维码主页:

    http://yourdomain/qrcode/


版本更改:
---------
- v1.0 模块名称更新为wechat_qrcode
