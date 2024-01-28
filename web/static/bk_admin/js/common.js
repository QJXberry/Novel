/**
 * Created by Sengo on 2017/7/12.
 */

function tip(cont, num) {
    layui.use(['layer'], function () {
            parent.layer.msg(cont, { icon: num, time: 1500 });
        });
}