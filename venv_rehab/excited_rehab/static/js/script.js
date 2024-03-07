
//送信
function posting(id) {
  var target = document.getElementById(id);
  target.method = "post";
  target.submit();
}

//ポップアップ
function popup(title, type, transmittable) {
  Swal.fire({
    title: title,
    timer: '1500',
    type: type,
    grow: 'row',
    customClass: 'customizable',
    showConfirmButton: false,
  }).then((result) => {
    posting(transmittable)
    $("#overlay").fadeIn(500);
  });
}

$(function () {
  ///////////////////////////////////////////////////////top画面のテキストエフェクト
  function randomCharactor(c) {
    //跳ねさせる要素をすべて取得
    var randomChar = document.getElementsByClassName(c);
    //for で総当たり
    for (var i = 0; i < randomChar.length; i++) {
      //クロージャー
      (function (i) {
        //i 番目の要素、テキスト内容、文字列の長さを取得
        var randomCharI = randomChar[i];
        var randomCharIText = randomCharI.textContent;
        var randomCharLength = randomCharIText.length;
        //何番目の文字を跳ねさせるかをランダムで決める
        var Num = ~~(Math.random() * randomCharLength);
        //跳ねさせる文字を span タグで囲む、それ以外の文字と合わせて再び文字列を作る
        var newRandomChar = randomCharIText.substring(0, Num) + "<span>" + randomCharIText.charAt(Num) + "</span>" + randomCharIText.substring(Num + 1, randomCharLength);
        randomCharI.innerHTML = newRandomChar;
        //アニメーションが終わったら再び関数を発火させる
        document.getElementsByClassName(c)[0].children[0].addEventListener("animationend", function () {
          setTimeout(function () {
            randomCharactor(c);
          }, 300);
        }, false)
      })(i)
    }
  }
  //クラス名が pyonpyon のクラスを跳ねさせる
  randomCharactor("pyonpyon");
  /////////////////////////////////////////////////////////////////////////////////


  //////////////////////// 変数に要素を入れる//////////////////
  //モーダル表示
  var open = $('.modal-open'),
    //モーダルクローズ
    close = $('.modal-close'),
    //戻るボタン
    back = $('.back'),
    container = $('.modal-container');
  modal_open_calendar = $('.modal-open_calendar')
  const dialog = document.querySelector('dialog');
  const text = document.getElementById('innerHTML');
  var flag
  flag = ""
  //ドメイン取得
  var pathname = location.pathname;
  //生年月日パリデーション
  const regex = /^[0-9]{4}\-(0[1-9]|1[0-2])\-(0[1-9]|[12][0-9]|3[01])$/;
  //メールアドレスパリデーション
  const pattern = /.+@.+\..+/;
  //育成画像４枚目のイメージ
  const done_image = document.getElementById("done_image")
  //育成要素達成かどうか
  const done = document.getElementById("done")
  //ホームボタン
  $('.home').on('click', function () {
    location.href = "/"
  })
  //ダイアログ、閉じるボタン
  $('.close').click(function () {
    $('.modal').fadeOut();
  })
  //モーダル、閉じるボタン
  close.on('click', function () {
    $('.modal').fadeOut();
  })


  //ログアウト処理
  if (pathname == '/' || pathname=='/supporter') {
    $(".logoutmodal-open").on('click', function () {
      text.innerHTML = "ログアウトしますか？"
      $('.modal').fadeIn();
      $(".post").on('click', function () {
        $('.modal').fadeOut();
        popup("ログアウト完了", "success", "submit")
      })
    })
  }


  if (done_image) {
    // promise化したfunction
    const loadImage = (src) => {
      return new Promise((resolve, reject) => {
        const img = new Image();
        img.onload = () => resolve(img);
        img.onerror = (e) => reject(e);
        img.src = src;
      });
    };
    // promise then/catch
    loadImage("static/" + done_image.value)
      .then(res => {
        Swal.fire({
          title: 'おめでとうございます！', text: '育成要素を達成しました。\nこのイメージはコレクションから確認できます。', imageUrl: "static/" + done_image.value, imageWidth: res.width, imageHeight: res.height, width: 800, customClass: 'customizable', imageAlt: 'Custom image',
        }).then((result) => {
          if (done.value) {
            Swal.fire({
              title: 'すべての育成要素を達成しました！', imageUrl: "static/images/training/comp.png", imageWidth: 800, imageHeight: 433, timer: '5000', grow: 'fullscreen', customClass: 'customizable', imageAlt: 'Custom image', showConfirmButton: false, animation: false
            }).then((result) => {
              location.href = "/"
            });
          }
        });
      })
  }

  //////////////////////////////////////////////////////////////////説明動画
  function aleat(test) {
    Swal.fire({
      imageUrl: test,
      grow: 'fullscreen',
      customClass: 'customizable',
      imageAlt: 'Custom image',
      confirmButtonText: '説明動画を閉じる'
    })
  }
  function aleatmanual(session, path) {
    if (!sessionStorage.getItem(session)) {
      aleat(path)
      sessionStorage.setItem(session, 'true')
    }
  }
  if (pathname == '/sns/menu/') {
    const path = document.getElementById("path").value;
    if (screen.width < 1000) {
      test = path + "/static/images/sns/SNS_mobile.gif"
    } else {
      test = path + "/static/images/sns/SNS_desktop.gif"
    }
    aleatmanual("sns", test)
    $('.replay').click(function () {
      aleat(test)
    })
  }
  if (pathname == '/diary/menu/') {
    const path = document.getElementById("path").value;
    if (screen.width < 1000) {
      test = path + "/static/images/diary/diary_mobile.gif"
    } else {
      test = path + "/static/images/diary/diary_desktop.gif"
    }
    aleatmanual("diary", test)
    $('.replay').click(function () {
      aleat(test)
    })
  }
  if (pathname == '/calendar/') {
    const path = document.getElementById("path").value;
    if (screen.width < 1000) {
      test = path + "/static/images/calendar/calendar_mobile.gif"
    } else {
      test = path + "/static/images/calendar/calendar_desktop.gif"
    }
    aleatmanual("calendar", test)
    $('.replay').click(function () {
      aleat(test)
    })
  }
  if (pathname == '/ToDO/menu/') {
    const path = document.getElementById("path").value;
    if (screen.width < 1000) {
      test = path + "/static/images/ToDO/ToDO_mobile.gif"
    } else {
      test = path + "/static/images/ToDO/ToDO_desktop.gif"
    }
    aleatmanual("ToDO", test)
    $('.replay').click(function () {
      aleat(test)
    })
  }
  ///////////////////////////////////////////////////////////////////////

  // SNS削除
  if (pathname == '/sns/reference/') {
    back.on('click', function () {
      location.href = "../menu"
    })
    const del = document.getElementById("del")
    delflag = sessionStorage.getItem('flag')
    if(del){
      if (!isNaN(del.value)) {
        text.innerHTML = "削除しますか？"
        $('.post').on('click', function () {
          posting("submit")
        })
        $('.modal').fadeIn();
        // dialog.showModal();
        sessionStorage.setItem('flag', 'true')
      } else if (delflag == 'true') {
      popup("削除完了", "success", "not")
    }
    }
  }
  // SNSスタンプ
  if (pathname == '/sns/timeline/') {
    document.getElementById("mainForm").onsubmit = function () {
      popup("送信完了", "success", "none")
    }
    back.on('click', function () {
      location.href = "../menu"
    })
  }

  //パスワード再設定
  if (pathname == '/allauth/password_reset/') {
    open.on('click', function () {
      if (form.Pw_reset_textbox.value.replace(/\s+/g, '') == "" || form.Pw_reset_check_textbox.value.replace(/\s+/g, '') == "" || form.Pw_reset_check_textbox.value.length > 10 || form.Pw_reset_check_textbox.value.length < 4 || form.Pw_reset_textbox.value != form.Pw_reset_check_textbox.value) {
        popup("正しく入力してください", "warning", "none")
        return false
      }
      else {
        popup("変更完了", "success", "submit")
      }

    })
  }
  //仮パスワード
  if (pathname == '/pass_conf') {
    open.on('click', function () {
      if (pattern.test(form.user_email_box.value) == false || form.user_id_textbox.value.replace(/\s+/g, '') == "") {
        popup("正しく入力してください", "warning", "none")
      } else {
        posting("submit")
      }
    })
    const no_id = document.getElementById("no_id").value;
    if (no_id == "error") {
      popup("正しく入力してください", "warning", "none")
    }
    return false
  }
  //初回パスワード登録
  if (pathname == '/allauth/first_password_set/') {
    open.on('click', function () {
      if (form.first_pw_id_textbox.value.replace(/\s+/g, '') == "" || form.first_pw_textbox.value.replace(/\s+/g, '') == "" || form.first_pw_check_textbox.value.replace(/\s+/g, '') == ""
        || form.first_pw_textbox.value != form.first_pw_check_textbox.value || form.first_pw_textbox.value.length < 4 || form.first_pw_textbox.value.length > 10) {
        popup("正しく入力してください", "warning", "none")
        return false
      }
    })
    const test = document.getElementById("test2").value;
    if (test == "test") {
      popup("正しく入力してください", "warning", "none")
    }
  }

  //ログイン
  if (pathname == '/allauth/login/' || pathname == '/') {
    open.on('click', function () {
      if (form.user_id_textbox.value.replace(/\s+/g, '') == "" || form.user_pw_textbox.value.replace(/\s+/g, '') == "" || form.user_pw_textbox.value.length > 10 || form.user_pw_textbox.value.length < 4) {
        popup("正しく入力してください", "warning", "none")
        return false
      }
    })
    const test = document.getElementById("login_error")
    if(test){
      if (test.value == 'login_error') {
        popup("正しく入力してください", "warning", "none")
      } else {
        Swal.fire({
          title: "仮パスワード発行完了", text: 'メールをご確認ください。', timer: '3000', type: 'success', grow: 'row', customClass: 'customizable', showConfirmButton: false,
        })
    }
    
    }
  }

  //戻る処理
  function back_func(form_name, locationname) {
    flag = "1"
    if (form_name.replace(/\s+/g, '') == "") {
      if (pathname == '/supporter/ToDO/') {
        location.href = "/"
      } else {
        location.href = locationname
      }

    } else {
      text.innerHTML = '戻りますか？';
      $('.modal').fadeIn();
    }
    $('.post').on('click', function () {
      if (flag != "2") {
        if (pathname == '/supporter/ToDO/') {
          location.href = "/"
        } else {
          location.href = locationname
        }
      }
    })
  }

  //戻る
  back.on('click', function () {
    flag = "1"
    if (pathname == '/experience/register' || pathname == '/experience/editing') {
      back_func(form.experience_inputbox.value, "/")
    }


    if (pathname == '/diary/post/') {
      back_func(form.diary_inputbox.value, "../menu")
    }

    if (pathname == '/diary/editing/') {
      const dary_editing = document.getElementById("dary_editing").value;
      if (dary_editing.length == 0) {
        location.href = "../reference"
      } else {
        text.innerHTML = '戻りますか？';
        $('.modal').fadeIn();
      }
      $('.post').on('click', function () {
        if (flag != "2") {
          location.href = "../reference"
        }
      })
    }
    if (pathname == '/diary/list/') {
      const diary_listid = document.getElementById("diary_list_id").value;
      if (diary_listid == 'k') {
        location.href = "../menu"
      } else {
        location.href = "/"
      }
    }
    if (pathname == '/diary/reference/') {
      location.href = "../list"
    }
    if (pathname == '/diary/menu/') {
      location.href = "../../"
    }
    if (pathname == '/ToDO/menu/') {
      location.href = "../../"
    }
    if (pathname == '/ToDO/reference/') {
      location.href = "../menu"
    }
    if (pathname == '/sns/menu/') {
      location.href = "../../"
    }
    if (pathname == '/sns/post/') {
      back_func(form.sns_inputbox.value, "../menu")
    }

    if (pathname == '/calendar/happy_rederence') {
      back_func(form.calendar_inputbox.value, "../calendar")
    }

    if (pathname == '/calendar/happy_editing') {
      back_func(form.calendar_editingbox.value, "../calendar/happy_rederence")
    }
    if (pathname == '/calendar/') {
      location.href = "../"
    }

    if (pathname == '/ToDO/add/' || pathname == "/supporter/ToDO/") {
      back_func(form.todo_inputbox.value, "/ToDO/menu/")
    }

    if (pathname == '/ToDO/list/') {
      location.href = "/ToDO/menu/"
    }
    if (pathname == '/ToDO/delete/') {
      location.href = "/ToDO/menu/"
    }
    if (pathname == '/allauth/info_change/') {
      location.href = "/allauth/info_confirmation/"
    }

    if (pathname == '/allauth/rehab_complete') {
      location.href = "/"
    }
    if (pathname == '/allauth/withdrawal') {
      location.href = "/"
    }
  })
  $('.back_calendar').click(function () {
    location.href = "/calendar/"
  })
  $('.back_expreience').click(function () {
    location.href = "/"
  })

  function post_func(form_name, innertext, title) {
    if (form_name.replace(/\s+/g, '') == "") {
      popup("正しく入力してください", "warning", "none")
    } else {
      text.innerHTML = innertext
      $('.modal').fadeIn();
    }
    $('.post').on('click', function () {
      if (flag != "1") {
        $('.modal').fadeOut();
        popup(title, 'success', "submit")
        if (pathname == '/sns/post/') {
          sessionStorage.removeItem('flag')
        }
      }
    })
  }
  //モーダル表示
  open.on('click', function () {
    flag = "2"
    // 日記投稿
    if (pathname == '/diary/post/') {
      post_func(form.diary_inputbox.value, "投稿しますか？", "投稿完了")
      return false;
    }

    //日記編集
    if (pathname == '/diary/editing/') {
      const dary_editing = document.getElementById("dary_editing").value;
      if (dary_editing.length == 0) {
        popup("正しく入力してください", "warning", "none")
      } else {
        text.innerHTML = '変更しますか？';
        $('.modal').fadeIn();
      }
      $('.post').on('click', function () {
        if (flag != "1") {
          $('.modal').fadeOut();
          popup("編集完了", "success", "submit")
        }

      })
    }


    //日記削除
    if (pathname == '/diary/reference/') {
      text.innerHTML = '削除しますか？';
      $('.modal').fadeIn();
      $('.post').on('click', function () {
        $('.modal').fadeOut();
        popup("削除完了", "success", "submit")
      })
    }

    //sns投稿
    if (pathname == '/sns/post/') {
      post_func(form.sns_inputbox.value, "投稿しますか？", "投稿完了")
      return false;
    }

    //カレンダー投稿
    if (pathname == '/calendar/happy_rederence') {
      post_func(form.calendar_inputbox.value, "登録しますか？", "登録完了")
      return false;
    }


    //カレンダー編集
    if (pathname == '/calendar/happy_editing') {
      post_func(form.calendar_editingbox.value, "変更しますか？", "編集完了")
      return false;
    }

    //todo削除
    if (pathname == '/ToDO/delete/') {
      if ($(".chk:checked").length > 0) {
        popup("削除完了", "success", "submit")
      } else {
        popup("正しく入力してください", "warning", "none")
      }
    }
    //todo完了
    if (pathname == '/ToDO/list/') {
      if ($(".chk:checked").length > 0) {
        popup("お疲れさまでした。", "success", "submit")
      } else {
        popup("正しく入力してください", "warning", "none")
      }
    }
    //ToDO追加
    if (pathname == '/ToDO/add/' || pathname == "/supporter/ToDO/") {
      $('.post').on('click', function () {
        if (flag != "1") {
          $('.modal').fadeOut();
          Swal.fire({ title: "追加完了", timer: '1500', type: 'success', grow: 'row', customClass: 'customizable', showConfirmButton: false }).then((result) => {
            if ($('.modal-wrapper:target').is(':visible')) {
              posting("submit2")
            } else {
              posting("submit")
            }
          });
        }
      })
      if ($('.modal-wrapper:target').is(':visible')) {
        if ($(".chk:checked").length > 0) {
          text.innerHTML = '追加しますか？';
          $('.modal').fadeIn();
        } else {
          popup("正しく入力してください", "warning", "none")
        }
      } else {
        if (form.todo_inputbox.value.replace(/\s+/g, '') == "") {
          popup("正しく入力してください", "warning", "none")
        } else {
          text.innerHTML = '追加しますか？';
          $('.modal').fadeIn();
        }
      }
    }

    //サインアップ
    if (pathname == '/allauth/signup/') {
      if (form.pw_textbox.value.replace(/\s+/g, '') == "" ||
        form.pw_check_textbox.value.replace(/\s+/g, '') == "" || form.pw_textbox.value != form.pw_check_textbox.value ||
        form.pw_textbox.value.length > 10 || form.pw_textbox.value.length < 4 || regex.test(form.birth_date.value) == false ||
        pattern.test(form.email_box.value) == false) {
        popup("正しく入力してください", "warning", "none")
      }
      else {
        container.addClass('active');
      }
      return false;
    }

    if (pathname == '/allauth/info_change') {
      if (regex.test(form.birth_date.value) == false) {
        popup("正しく入力してください", "warning", "none")
      } else {
        text.innerHTML = '変更しますか？';
        $('.modal').fadeIn();
      }
      $('.info_change').click(function () {
        $('.modal').fadeOut();
        popup("変更完了", "success", "submit")

      })
    }

    if (pathname == '/allauth/rehab_complete') {
      Swal.fire({
        title: 'リハビリ完了\nおめでとうございます。', showConfirmButton: false, customClass: 'customizable', grow: 'fullscreen', timer: '4000',
      }).then((result) => {
        posting("submit")
      });
    }
    if (pathname == '/allauth/withdrawal') {
      Swal.fire({
        title: '退会が完了しました', html: 'ご利用いただき、誠にありがとうございました。', showConfirmButton: false, customClass: 'customizable', grow: 'fullscreen', timer: '4000',
      }).then((result) => {
        posting("submit")
      });
    }

    //経験談
    if (pathname == '/experience/register') {
      post_func(form.experience_inputbox.value, "登録しますか？", "登録完了")
    }
    if (pathname == '/experience/editing') {
      post_func(form.experience_inputbox.value, "変更しますか？", "編集完了")
    }

    if (pathname == '/id_conf') {
      if (pattern.test(form.email_box.value) == false) {
        popup("正しく入力してください", "warning", "none")
      } else {
        posting("submit")
      }
      return false
    }

  });
  //エンター無効
  if (pathname == '/ToDO/add/' || pathname == "/supporter/ToDO/") {
    $(function () {
      $("input").on("keydown", function (e) {
        if ((e.which && e.which === 13) || (e.keyCode && e.keyCode === 13)) {
          return false;
        } else {
          return true;
        }
      });
    });
  }

  //カレンダー削除
  modal_open_calendar.on('click', function () {
    text.innerHTML = '削除しますか？';
    $('.modal').fadeIn();
    $(".post").on('click', function () {
      $('.modal').fadeOut();
      popup("削除完了", "success", "submit")
    })
  })
  //モーダルの外側をクリックしたらモーダルを閉じる
  $(document).on('click', function (e) {
    if (!$(e.target).closest('.modal-body').length) {
      container.removeClass('active');
    }
  });
  close.on('click', function () {
    container.removeClass('active');
    dialog.close();
  })
});

function PageTopAnime() {
  var scroll = $(window).scrollTop();
  if (scroll >= 100) {//上から100pxスクロールしたら
    $('#page-top').removeClass('DownMove');//#page-topについているDownMoveというクラス名を除く
    $('#page-top').addClass('UpMove');//#page-topについているUpMoveというクラス名を付与
  } else {
    if ($('#page-top').hasClass('UpMove')) {//すでに#page-topにUpMoveというクラス名がついていたら
      $('#page-top').removeClass('UpMove');//UpMoveというクラス名を除き
      $('#page-top').addClass('DownMove');//DownMoveというクラス名を#page-topに付与
    }
  }
}
// 画面をスクロールをしたら動かしたい場合の記述
$(window).scroll(function () {
  PageTopAnime();/* スクロールした際の動きの関数を呼ぶ*/
});
// ページが読み込まれたらすぐに動かしたい場合の記述
$(window).on('load', function () {
  PageTopAnime();/* スクロールした際の動きの関数を呼ぶ*/
});
// #page-topをクリックした際の設定
$('#page-top').click(function () {
  var scroll = $(window).scrollTop(); //スクロール値を取得
  if (scroll > 0) {
    $(this).addClass('floatAnime');//クリックしたらfloatAnimeというクラス名が付与
    $('body,html').animate({
      scrollTop: 0
    }, 2000, function () {//スクロールの速さ。数字が大きくなるほど遅くなる
      $('#page-top').removeClass('floatAnime');//上までスクロールしたらfloatAnimeというクラス名を除く
    });
  }
  return false;//リンク自体の無効化
});


