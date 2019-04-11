$(function () {
    // 1 查询省
    var $pro = $('#pro');
    // 查询省信息，获得JSON格式的数据 data={'data':[]}
    $.get('/area-pro/', function(data) {
        console.log('get pro');
        // 遍历JSON
        $.each(data.data, function (index, item) {

            // 文档节点编辑 item=[id, title]
            $pro.append(
                // value = id，好处是id是unique的，防止 省：北京市 市：北京市，这种出现混淆
                '<option value="' + item[0] + '">' + item[1] + '</option>'
            );

        });
    });

    // 2 查询市
    var $city = $('#city');
    // 根据用户选定省份，生成市列表
    $pro.change(function () {
        console.log('pro change');

        // 清楚之前的数据
        $city.empty().append('<option value="0">请选择市</option>');

        // $(this) -> 当前选中的selectElement，不是optionElement
        var url = '/area-city-'+$(this).val()+'/';
        $.get(url, function (data) {
            $.each(data.data, function (index, item) {
                $city.append('<option value="' + item.id + '">' + item.title + '</option>');
            });
        });

    });

    // 3 查询区，根据用户选定的城市查询区
    var $dis = $('#dis')
    $city.change(function () {
        // 清楚之前的数据
        $dis.empty().append('<option value="0">请选择区</option>');

        // $(this) -> 当前选中的selectElement，不是optionElement
        var url = '/area-city-'+$(this).val()+'/';
        $.get(url, function (data) {
            $.each(data.data, function (index, item) {
                $dis.append('<option value="' + item.id + '">' + item.title + '</option>');
            });
        });
    });

});
