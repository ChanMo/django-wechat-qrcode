基于django_wechat_member的二维码模块
=====================================

一个基于 `django_wechat_member <http://github.com/ChanMo/django_wechat_member/>`_ 的二维码模块

功能说明：
----------

- 每个微信会员有一个唯一的二维码
- 可以记录用户的来源

快速开始:
---------

安装 *django-wechate-qrcode* :

.. code-block::

    pip install django-wechat-qrcode

修改 *settings.py* 文件:

.. code-block::

    INSTALLED_APPS = (
        ...
        'qrcode',
        ...
    )

修改 *urls.py* 文件:

.. code-block::

    url(r'^qrcode/', include('qrcode.urls')),

更新数据库:

.. code-block::

   python manage.py migrate

微信开发者链接:

    http://yourdomain/qrcode/api/

用户二维码主页:

    http://yourdomain/qrcode/


版本更改:
---------
- v0.1 第一版
