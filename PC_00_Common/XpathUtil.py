from lxml.etree import Element

from A_03_Common.ComLog import logger


class XpathUtil:

    def get_unique(self, element: Element, xpath, msg=''):
        try:
            result_list = element.xpath(xpath)
            if result_list:
                return result_list[0]
            else:
                return ''
        except AttributeError as e:
            logger.error(f"xpath解析失败, 出现异常, 传入的element没有xpath属性: msg: {msg}"
                         f"\n\t异常: {e}"
                         f"\n\telement: {element} type: {type(element)}"
                         f"\n\txpath: {xpath}")
            return None


xpath_util = XpathUtil()
