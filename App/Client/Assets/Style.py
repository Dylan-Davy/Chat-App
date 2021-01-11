qss = '''/*Copyright (c) DevSec Studio. All rights reserved.

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

/*-----QWidget-----*/
QWidget
{
	background-color: #232430;
	color: #000000;
	border-color: #000000;

}

/*-----QFrame-----*/
QFrame
{
	background-color: #ff9c2b;
}


/*-----QLabel-----*/
QLabel
{
	background-color: rgba(0,0,0,0%);
	color: #c1c1c1;
	border-color: #000000;

}


/*-----QPushButton-----*/
QPushButton
{
	background-color: #ff9c2b;
	color: #000000;
	font-weight: bold;
	border-style: solid;
	border-color: #000000;
	padding: 6px;

}


QPushButton::hover
{
	background-color: #ffaf5d;

}


QPushButton::pressed
{
	background-color: #dd872f;

}


/*-----QToolButton-----*/
QToolButton
{
	background-color: #ff9c2b;
	color: #000000;
	font-weight: bold;
	border-style: solid;
	border-color: #000000;
	padding: 6px;

}


QToolButton::hover
{
	background-color: #ffaf5d;

}


QToolButton::pressed
{
	background-color: #dd872f;

}


/*-----QLineEdit-----*/
QLineEdit
{
	background-color: #38394e;
	color: #c1c1c1;
	border-style: solid;
	border-width: 1px;
	border-color: #4a4c68;

}


/*-----QTableView-----*/
QTableView, 
QHeaderView, 
QTableView::item 
{
	background-color: #232430;
	color: #c1c1c1;
	border: none;

}


QTableView::item:selected 
{ 
    background-color: #41424e;
    color: #c1c1c1;

}


QHeaderView::section:horizontal 
{
    background-color: #232430;
	border: 1px solid #37384d;
	padding: 5px;

}


QTableView::indicator{
	background-color: #1d1d28;
	border: 1px solid #37384d;

}


QTableView::indicator:checked{
	image:url("./ressources/check.png"); /*To replace*/
	background-color: #1d1d28;

}

/*-----QTabWidget-----*/
QTabWidget::pane 
{ 
    border: none;

}


QTabWidget::tab-bar 
{
    left: 5px; 

}


QTabBar::tab 
{
    color: #c1c1c1;
    min-width: 1px;
	padding-left: 25px;
	margin-left:-22px;
    height: 28px;
	border: none;

}


QTabBar::tab:selected 
{
    color: #c1c1c1;
	font-weight: bold;
    height: 28px;

}


QTabBar::tab:!first 
{
    margin-left: -20px;

}


QTabBar::tab:hover 
{
    color: #DDD;

}


/*-----QScrollBar-----*/
QScrollBar:horizontal 
{
    background-color: transparent;
    height: 8px;
    margin: 0px;
    padding: 0px;

}


QScrollBar::handle:horizontal 
{
    border: none;
	min-width: 100px;
    background-color: #56576c;

}


QScrollBar::add-line:horizontal, 
QScrollBar::sub-line:horizontal,
QScrollBar::add-page:horizontal, 
QScrollBar::sub-page:horizontal 
{
    width: 0px;
    background-color: transparent;

}


QScrollBar:vertical 
{
    background-color: transparent;
    width: 8px;
    margin: 0;

}


QScrollBar::handle:vertical 
{
    border: none;
	min-height: 100px;
    background-color: #56576c;

}


QScrollBar::add-line:vertical, 
QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical, 
QScrollBar::sub-page:vertical 
{
    height: 0px;
    background-color: transparent;

}
'''