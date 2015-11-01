# securities
some simple model for securities and mapping to relational databases with sqlachemy

Задание я выполнил не совсем так, как было написано. О причинах вкратце писал еще до выполнения, но повторю на всякий случай почему сделано так, а не иначе.

Во-первых, full_name, short_name, latin_name объеденины в класс Issuer (Whole Value pattern).
Поскольу не знаю бизнес-правил, то выделять в отдельную entity не стал.
Если один и тот же Issuer может выпускать разные бумаги и они будут в одном bounded context, то имеет смысл использовать OneToMany Relationship.

Во-вторых, face_value и face_value_unit - это тоже Whole Value. Поэтому использовал готовую реализацию Money pattern.

В-третьих поскольку внешний класс (Money) без патчинга или написания wrapper-a замапить как CompositeColumn в sqlalchemy видимо нельзя (кстати, в отличие от ORM в java, где все это можно сделать с помощью внешней конфигурации), то я решил сделать проще - factory method и property decorator.

Из-за этого в get_or_create можно получить не до конца сконфигурированный объект, что не есть хорошо.
Впрочем, это можно решить написанием класса обертки, просто я не стал тратить на это время в задании.
