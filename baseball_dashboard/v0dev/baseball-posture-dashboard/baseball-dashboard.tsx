"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Activity,
  Target,
  TrendingUp,
  Camera,
  Play,
  Pause,
  RotateCcw,
  AlertTriangle,
  CheckCircle,
  User,
  Calendar,
  BarChart3,
} from "lucide-react"

export default function Component() {
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [currentScore, setCurrentScore] = useState(85)
  const [analysisData, setAnalysisData] = useState({
    stance: { score: 88, status: "良好" },
    balance: { score: 82, status: "需改善" },
    armPosition: { score: 91, status: "優秀" },
    footwork: { score: 79, status: "需改善" },
    timing: { score: 86, status: "良好" },
  })

  const [recentAnalyses] = useState([
    { date: "2024-01-15", score: 85, type: "打擊姿勢" },
    { date: "2024-01-14", score: 78, type: "投球姿勢" },
    { date: "2024-01-13", score: 92, type: "打擊姿勢" },
    { date: "2024-01-12", score: 81, type: "守備姿勢" },
    { date: "2024-01-11", score: 87, type: "打擊姿勢" },
  ])

  const toggleAnalysis = () => {
    setIsAnalyzing(!isAnalyzing)
  }

  const getScoreColor = (score: number) => {
    if (score >= 90) return "text-green-600"
    if (score >= 80) return "text-yellow-600"
    return "text-red-600"
  }

  const getStatusBadge = (status: string) => {
    const variants = {
      優秀: "default",
      良好: "secondary",
      需改善: "destructive",
    } as const
    return variants[status as keyof typeof variants] || "secondary"
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">棒球姿勢分析儀表板</h1>
            <p className="text-gray-600 mt-1">即時動作分析與技術改善建議</p>
          </div>
          <div className="flex items-center gap-3">
            <Badge variant="outline" className="px-3 py-1">
              <User className="w-4 h-4 mr-1" />
              選手: 張小明
            </Badge>
            <Badge variant="outline" className="px-3 py-1">
              <Calendar className="w-4 h-4 mr-1" />
              {new Date().toLocaleDateString("zh-TW")}
            </Badge>
          </div>
        </div>

        {/* Real-time Analysis Section */}
        <Card className="border-2 border-blue-200">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Camera className="w-5 h-5" />
              即時姿勢分析
            </CardTitle>
            <CardDescription>使用AI視覺技術即時分析棒球動作姿勢</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Camera Feed Placeholder */}
              <div className="relative">
                <div className="aspect-video bg-gray-900 rounded-lg flex items-center justify-center">
                  <div className="text-center text-white">
                    <Camera className="w-12 h-12 mx-auto mb-2 opacity-50" />
                    <p className="text-sm opacity-75">攝影機畫面</p>
                    {isAnalyzing && (
                      <div className="absolute top-4 right-4">
                        <div className="flex items-center gap-2 bg-red-600 px-3 py-1 rounded-full">
                          <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
                          <span className="text-xs">錄製中</span>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
                <div className="flex justify-center gap-2 mt-4">
                  <Button onClick={toggleAnalysis} className="flex items-center gap-2">
                    {isAnalyzing ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                    {isAnalyzing ? "暫停分析" : "開始分析"}
                  </Button>
                  <Button variant="outline" className="flex items-center gap-2">
                    <RotateCcw className="w-4 h-4" />
                    重置
                  </Button>
                </div>
              </div>

              {/* Current Analysis */}
              <div className="space-y-4">
                <div className="text-center">
                  <div className={`text-4xl font-bold ${getScoreColor(currentScore)}`}>{currentScore}</div>
                  <p className="text-gray-600">整體姿勢評分</p>
                </div>

                <div className="space-y-3">
                  {Object.entries(analysisData).map(([key, data]) => (
                    <div key={key} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div className="flex items-center gap-3">
                        <div
                          className={`w-3 h-3 rounded-full ${
                            data.score >= 90 ? "bg-green-500" : data.score >= 80 ? "bg-yellow-500" : "bg-red-500"
                          }`}
                        ></div>
                        <span className="font-medium">
                          {key === "stance"
                            ? "站姿"
                            : key === "balance"
                              ? "平衡"
                              : key === "armPosition"
                                ? "手臂位置"
                                : key === "footwork"
                                  ? "腳步"
                                  : "時機掌握"}
                        </span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className={`font-bold ${getScoreColor(data.score)}`}>{data.score}</span>
                        <Badge variant={getStatusBadge(data.status)}>{data.status}</Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Analysis Tabs */}
        <Tabs defaultValue="metrics" className="space-y-4">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="metrics">關鍵指標</TabsTrigger>
            <TabsTrigger value="history">歷史記錄</TabsTrigger>
            <TabsTrigger value="recommendations">改善建議</TabsTrigger>
          </TabsList>

          <TabsContent value="metrics" className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">平均評分</CardTitle>
                  <Target className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">84.2</div>
                  <p className="text-xs text-muted-foreground">+2.1% 較上週</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">分析次數</CardTitle>
                  <Activity className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">127</div>
                  <p className="text-xs text-muted-foreground">本月總計</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">改善率</CardTitle>
                  <TrendingUp className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">+12%</div>
                  <p className="text-xs text-muted-foreground">較上月提升</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">最佳項目</CardTitle>
                  <CheckCircle className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">手臂位置</div>
                  <p className="text-xs text-muted-foreground">平均 91 分</p>
                </CardContent>
              </Card>
            </div>

            {/* Progress Bars */}
            <Card>
              <CardHeader>
                <CardTitle>各項目表現趨勢</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {Object.entries(analysisData).map(([key, data]) => (
                  <div key={key} className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>
                        {key === "stance"
                          ? "站姿"
                          : key === "balance"
                            ? "平衡"
                            : key === "armPosition"
                              ? "手臂位置"
                              : key === "footwork"
                                ? "腳步"
                                : "時機掌握"}
                      </span>
                      <span className="font-medium">{data.score}%</span>
                    </div>
                    <Progress value={data.score} className="h-2" />
                  </div>
                ))}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="history" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BarChart3 className="w-5 h-5" />
                  最近分析記錄
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {recentAnalyses.map((analysis, index) => (
                    <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                      <div className="flex items-center gap-3">
                        <div
                          className={`w-3 h-3 rounded-full ${
                            analysis.score >= 90
                              ? "bg-green-500"
                              : analysis.score >= 80
                                ? "bg-yellow-500"
                                : "bg-red-500"
                          }`}
                        ></div>
                        <div>
                          <p className="font-medium">{analysis.type}</p>
                          <p className="text-sm text-gray-600">{analysis.date}</p>
                        </div>
                      </div>
                      <div className={`text-lg font-bold ${getScoreColor(analysis.score)}`}>{analysis.score}</div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="recommendations" className="space-y-4">
            <div className="grid gap-4">
              <Card className="border-yellow-200 bg-yellow-50">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-yellow-800">
                    <AlertTriangle className="w-5 h-5" />
                    需要改善的項目
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="p-3 bg-white rounded border-l-4 border-yellow-400">
                    <h4 className="font-medium text-yellow-800">平衡控制 (82分)</h4>
                    <p className="text-sm text-gray-600 mt-1">建議加強核心肌群訓練，練習單腳站立平衡動作</p>
                  </div>
                  <div className="p-3 bg-white rounded border-l-4 border-yellow-400">
                    <h4 className="font-medium text-yellow-800">腳步移動 (79分)</h4>
                    <p className="text-sm text-gray-600 mt-1">注意重心轉移，練習步伐的節奏和時機</p>
                  </div>
                </CardContent>
              </Card>

              <Card className="border-green-200 bg-green-50">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-green-800">
                    <CheckCircle className="w-5 h-5" />
                    表現優秀的項目
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="p-3 bg-white rounded border-l-4 border-green-400">
                    <h4 className="font-medium text-green-800">手臂位置 (91分)</h4>
                    <p className="text-sm text-gray-600 mt-1">手臂擺放位置標準，保持現有動作模式</p>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>訓練建議</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-start gap-3">
                      <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                        <span className="text-xs font-bold text-blue-600">1</span>
                      </div>
                      <div>
                        <h4 className="font-medium">每日平衡訓練</h4>
                        <p className="text-sm text-gray-600">進行15分鐘的平衡球訓練</p>
                      </div>
                    </div>
                    <div className="flex items-start gap-3">
                      <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                        <span className="text-xs font-bold text-blue-600">2</span>
                      </div>
                      <div>
                        <h4 className="font-medium">腳步練習</h4>
                        <p className="text-sm text-gray-600">重複練習基本步伐移動</p>
                      </div>
                    </div>
                    <div className="flex items-start gap-3">
                      <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                        <span className="text-xs font-bold text-blue-600">3</span>
                      </div>
                      <div>
                        <h4 className="font-medium">影片回放分析</h4>
                        <p className="text-sm text-gray-600">觀看慢動作回放找出問題點</p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
