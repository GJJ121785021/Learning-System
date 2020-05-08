new Vue({
    el: '#choose_order',
    data: {
        // 默认排序方式， 默认数据, 默认页面
        now_order: '按最新',
        data: null,
        now_page: 1,
        previous_button: 'page-item disabled',
        next_button: 'page-item',

    },
    mounted() {
        // 请求数据
        this.get_words('/english_app/words.json');
    },
    methods: {
        // 请求数据
        get_words: function (url, into_full_url = null) {
            if (into_full_url) {
                full_url = into_full_url
            } else {
                full_url = location.origin + url;
            }

            let that = this;
            axios
                .get(full_url)
                .then(function (response) {
                    that.data = response.data;
                    // console.log(response.data.results);
                    // 检查上下页按钮的有效性
                    if (response.data.previous) {
                        that.previous_button = 'page-item'
                    } else {
                        that.previous_button = 'page-item disabled'
                    }
                    if (response.data.next) {
                        that.next_button = 'page-item'
                    } else {
                        that.next_button = 'page-item disabled'
                    }

                })
                .catch(
                    function (error) {
                        console.log(error)
                    }
                )

        },
        // 排序方式：按最新
        new_order: function () {
            let my_order = '按最新';
            if (this.now_order !== my_order) {
                this.now_order = my_order;
                // 请求数据
                this.get_words('/english_app/words.json');
            }
            this.now_page = 1
        },
        // 排序方式：按字母顺序
        word_abc_order: function () {
            let my_order = '按字母顺序';
            if (this.now_order !== my_order) {
                this.now_order = my_order;
                // 请求数据
                this.get_words('/english_app/words.json?ordering=english');
            }
            this.now_page = 1
        },
        // 排序方式：按错误率
        error_rate_order: function () {
            let my_order = '按错误率';
            if (this.now_order !== my_order) {
                this.now_order = my_order;
                // 请求数据
                this.get_words('/english_app/words.json?ordering=error_odds');
            }
            this.now_page = 1
        },
        // 修改表格的颜色
        get_class_for_show: function (n) {
            if (n % 4 === 0) {
                return 'success'
            } else if (n % 4 === 1) {
                return 'error'
            } else if (n % 4 === 2) {
                return 'success'
            } else {
                return 'info'
            }
        },
        // 上一页
        previous_page: function () {
            if (this.data.previous) {
                this.get_words(null, this.data.previous);
                this.now_page--;

            }
        },
        // 下一页
        next_page: function () {
            if (this.data.next) {
                this.get_words(null, this.data.next);
                this.now_page++;
            }


        },
    },
});