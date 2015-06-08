<!DOCTYPE html>
<html class="no-js">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title></title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <link rel="stylesheet" href="css/bootstrap.min.css">
        <link rel="stylesheet" href="css/bootstrap-theme.min.css">
        <link rel="stylesheet" href="css/main.css">
        <style type="text/css">
            #all_forms .form-horizontal .control-label{
                text-align: left !important;
            }
        </style>

        <script src="js/vendor/modernizr-2.6.2-respond-1.1.0.min.js"></script>
    </head>
    <body>

    <!-- Main jumbotron for a primary marketing message or call to action -->
    <div class="jumbotron">
      <div class="container">
        <h1>Анализ поэтических текстов онлайн</h1>
        <p>Введите необходимые данные в столбце слева и нажмите "Анализ"</p>
        <p>Перейти в раздел <a href="phonetic_analysis/">фонетического разбора</a></p>
      </div>
    </div>

    <div class="container">
      <!-- Example row of columns -->
      <div class="row" id="all_forms">
          <div class="col-md-6 alert-info alert">
              <div class="col-sm-12"><h2 class="text-center">Входные данные</h2></div>
              <!--<div class="col-sm-8"><h3>Показатель</h3></div>-->
              <!--<div class="col-sm-4"><h3>Значение</h3></div>-->
              <form class="form-horizontal" role="form" id="form1">
                  <div class="form-group">
                      <label for="direction" class="col-sm-4 control-label">Текст стихотворения*</label>
                      <div class="col-sm-8">
                          <!--<input type="text" class="form-control" id="inputEmail3">-->
                          <textarea class="form-control" rows="20" id="poem_body"></textarea>
                      </div>
                  </div>
                  <div class="form-group">
                      <label for="cities" class="col-sm-4 control-label">Название стихотворения</label>
                      <div class="col-sm-8">
                          <input type="text" class="form-control typeahead" id="cities" autocomplete="off" />
                          <!--<datalist id="cities_list"></datalist>-->
                      </div>
                  </div>
                  <div class="form-group">
                      <label for="population" class="col-sm-4 control-label">Год создания</label>
                      <div class="col-sm-8">
                          <input type="text" class="form-control" id="population">
                      </div>
                  </div>
                  <div class="form-group">
                      <label for="count_of_pos" class="col-sm-4 control-label">Автор произведения</label>
                      <div class="col-sm-8">
                          <input type="text" class="form-control" id="count_of_pos">
                      </div>
                  </div>
                  <div class="form-group">
                      <div class="col-sm-offset-4 col-sm-4">
                          <button type="button" id="count_now" class="btn btn-default">Анализ</button>
                      </div>
                      <div class="col-sm-4">
                          <button type="reset" class="btn btn-default" id="reset1">Очистить</button>
                      </div>
                  </div>
              </form>
          </div>
          <div class="col-md-1"></div>

          <div class="col-md-5 alert-success alert">
              <div class="col-sm-12"><h2 class="text-center">Результат</h2></div>
              <!--<div class="col-sm-8"><h3>Показатель</h3></div>-->
              <!--<div class="col-sm-4"><h3>Значение</h3></div>-->
              <form class="form-horizontal" role="form">
                  <div class="form-group">
                      <label for="Y1" class="col-sm-8 control-label">метрика стихотворения и стопность</label>
                      <div class="col-sm-4">
                          <input type="text" class="form-control" id="Y1" disabled>
                      </div>
                  </div>
                  <div class="form-group">
                      <label for="Y2" class="col-sm-8 control-label">количество строк, без учета пустых</label>
                      <div class="col-sm-4">
                          <input type="text" class="form-control" id="Y2" disabled>
                      </div>
                  </div>
                  <div class="form-group">
                      <label for="Y3" class="col-sm-8 control-label">рифмовка строфики</label>
                      <div class="col-sm-4">
                          <input type="text" class="form-control" id="Y3" disabled>
                      </div>
                  </div>
                  <div class="form-group">
                      <label for="Y4" class="col-sm-8 control-label">количество мужских окончаний последних слов в стихотворных строках</label>
                      <div class="col-sm-4">
                          <input type="text" class="form-control" id="Y4" disabled>
                      </div>
                  </div>
                  <!-- NEW 5 -->
                  <div class="form-group">
                      <label for="Y5" class="col-sm-8 control-label">количество женских окончаний последних слов в стихотворных строках</label>
                      <div class="col-sm-4">
                          <input type="text" class="form-control" id="Y5" disabled>
                      </div>
                  </div>
                  <div class="form-group">
                      <label for="Y6" class="col-sm-8 control-label">количество дактилических и др. окончаний последних слов в стихотворных строках</label>
                      <div class="col-sm-4">
                          <input type="text" class="form-control" id="Y6" disabled>
                      </div>
                  </div>
                  <div class="form-group">
                      <label for="Y7" class="col-sm-8 control-label">количество нерифмованных мужских окончаний</label>
                      <div class="col-sm-4">
                          <input type="text" class="form-control" id="Y7" disabled>
                      </div>
                  </div>
                  <div class="form-group">
                      <label for="Y8" class="col-sm-8 control-label">количество нерифмованных женских окончаний</label>
                      <div class="col-sm-4">
                          <input type="text" class="form-control" id="Y8" disabled>
                      </div>
                  </div>
                  <div class="form-group">
                      <label for="Y9" class="col-sm-8 control-label">количество нерифмованных дактилических и др окончаний</label>
                      <div class="col-sm-4">
                          <input type="text" class="form-control" id="Y9" disabled>
                      </div>
                  </div>
                  <div class="form-group">
                      <label for="Y10" class="col-sm-8 control-label">количество строк без конечных слов</label>
                      <div class="col-sm-4">
                          <input type="text" class="form-control" id="Y10" disabled>
                      </div>
                  </div>
                  <div class="form-group">
                      <label for="Y11" class="col-sm-8 control-label"
                             title="sss"
                             data-toggle="popover"
                             data-trigger="focus"
                             data-content="some content">
                          тип строфической формы
                          <button type="button" id="help_Y11" class="btn btn-xs btn-default"
                             data-toggle="popover"
                             data-trigger="hover"
                             data-placement="left"
                             title="тип строфической формы"
                             data-content="<ol><li>стихотворения, состоящие из одной строфы (восемь строк или меньше)</li><li>правильно повторяющиеся строфы</li><li>вольные станцы</li><li>парная рифмовка</li><li>вольная рифмовка</li></ol>">?</button>
                      </label>
                      <div class="col-sm-4">
                          <input type="text" class="form-control" id="Y11" disabled>
                      </div>
                  </div>

                  <!-- END NEW 5 -->
                  <div class="form-group">
                      <div class="col-sm-12">
<!--                          <button type="button" id="count_now" class="btn btn-default">Анализ</button>-->
                          <div class="accent_wrap"></div>
                          <div class="accent_sign"></div>
                      </div>
                  </div>
              </form>
          </div>
      </div>

      <hr>

      <footer>
        <p>ИВТ СО РАН</p>
        <p>&copy; lvla.ru</p>
      </footer>
    </div> <!-- /container -->

        <script src="js/vendor/jquery-1.11.0.min.js"></script>
        <!--<script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>-->
        <!--<script>window.jQuery || document.write('<script src="js/vendor/jquery-1.11.0.min.js"><\/script>')</script>-->

        <script src="js/vendor/bootstrap.min.js"></script>
        <script src="js/vendor/typeahead.bundle.js"></script>

        <!--<script src="js/data.js"></script>-->
        <script src="js/main.js?r=2"></script>
    </body>
</html>
